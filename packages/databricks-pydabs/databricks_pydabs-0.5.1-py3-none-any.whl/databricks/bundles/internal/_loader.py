import inspect
import logging
import traceback
from io import StringIO
from typing import Any, Callable, Optional

from databricks.bundles.internal._diagnostics import (
    Diagnostic,
    Diagnostics,
    Location,
    Severity,
)
from databricks.bundles.jobs import Job, JobSyntaxError
from databricks.bundles.jobs.functions.job import JobFunction
from databricks.bundles.resource import Resource, ResourceGenerator, ResourceMutator


class _Loader:
    """
    Loader reads resources, resource generators and mutators from Python modules and YAML files.

    Mutators and resource generators are only loaded, and not applied.
    """

    def __init__(self):
        self._jobs = dict[str, Job]()
        self._mutators = list[ResourceMutator]()
        self._resource_generators = list[ResourceGenerator]()

    @property
    def jobs(self) -> dict[str, Job]:
        return self._jobs

    @property
    def mutators(self) -> list[ResourceMutator]:
        return self._mutators

    @property
    def resource_generators(self) -> list[ResourceGenerator]:
        return self._resource_generators

    def register_module(self, module: Any, *, override: bool) -> Diagnostics:
        diagnostics = Diagnostics()

        for _, resource in _getmembers_ordered(module, _is_resource):
            logging.debug("Discovered job %s", resource.resource_name)

            diagnostics = diagnostics.extend(
                self.register_job(resource, override=override)
            )

        for _, mutator in _getmembers_ordered(module, _is_mutator):
            if mutator in self._mutators:
                continue

            logging.debug("Discovered resource mutator %s", mutator.function.__name__)

            self._mutators.append(mutator)

        for _, generator in _getmembers_ordered(module, _is_resource_generator):
            if generator in self._resource_generators:
                continue

            logging.debug(
                "Discovered resource generator %s", generator.function.__name__
            )

            self._resource_generators.append(generator)

        return diagnostics

    def register_bundle_config(self, bundle: dict) -> Diagnostics:
        diagnostics = Diagnostics()
        jobs_dict = bundle.get("resources", {}).get("jobs", {})

        for resource_name, job_dict in jobs_dict.items():
            try:
                job = Job.create(resource_name=resource_name, **job_dict)
            except Exception as exc:
                return diagnostics.extend(
                    Diagnostics.from_exception(
                        exc=exc,
                        summary="Error while loading job",
                        path=f"resources.jobs.{resource_name}",
                    )
                )

            diagnostics = diagnostics.extend(self.register_job(job, override=False))

        return diagnostics

    def register_job(self, job: Job, *, override: bool) -> Diagnostics:
        diagnostics = Diagnostics()

        if not job.resource_name:
            return diagnostics.extend(
                Diagnostics.create_error(
                    msg="resource_name is required for a job",
                    location=_find_job_location(job),
                )
            )

        existing_job = self._jobs.get(job.resource_name)

        if existing_job and not override:
            location = _find_job_location(job) or _find_job_location(existing_job)

            return diagnostics.extend(
                Diagnostics.create_error(
                    msg=f"Two jobs have the same resource_name '{job.resource_name}'",
                    location=location,
                )
            )

        # evaluate ".tasks" because they are lazily evaluated and can throw
        # exceptions when DAG has errors
        try:
            job.tasks
        except JobSyntaxError as exc:
            return diagnostics.extend(_translate_job_syntax_error(exc))
        except Exception as exc:
            return diagnostics.extend(
                Diagnostics.from_exception(
                    exc=exc,
                    summary=f"Error while loading job '{job.resource_name}'",
                    location=_find_job_location(job),
                )
            )

        # FIXME this generates duplicate warnings, because when we override
        # job after mutators we have the same diagnostics as before
        # we deduplicate it in _remove_known_warnings for now
        if isinstance(job, JobFunction):
            location = _find_job_location(job)
            job_diagnostics = job._diagnostics.with_location_if_absent(location)

            diagnostics = diagnostics.extend(job_diagnostics)

        self._jobs[job.resource_name] = job

        return diagnostics


def _find_job_location(job: Job) -> Optional[Location]:
    if isinstance(job, JobFunction):
        return Location.from_callable(job.function)

    return None


def _translate_job_syntax_error(exc: JobSyntaxError) -> Diagnostics:
    detail = StringIO()
    detail.writelines(traceback.format_exception_only(exc))

    location = (
        Location(
            file=exc.filename,
            line=exc.lineno or 1,
            column=exc.offset or 1,
        )
        if exc.filename
        else None
    )

    return Diagnostics(
        items=[
            Diagnostic(
                severity=Severity.ERROR,
                summary=exc.msg,
                detail=detail.getvalue(),
                location=location,
            )
        ]
    )


def _is_resource(obj):
    return isinstance(obj, Resource)


def _is_resource_generator(obj):
    return isinstance(obj, ResourceGenerator)


def _is_mutator(obj):
    return isinstance(obj, ResourceMutator)


def _getmembers_ordered(obj, predicate: Callable[[Any], bool]):
    """Get members in the order they are defined in the module."""

    members = inspect.getmembers(obj, predicate)
    priority = {key: idx for idx, key in enumerate(vars(obj).keys())}

    members.sort(key=lambda kv: priority.get(kv[0], 0))

    return members
