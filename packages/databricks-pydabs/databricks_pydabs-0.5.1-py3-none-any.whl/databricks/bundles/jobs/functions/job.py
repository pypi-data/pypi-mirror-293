from dataclasses import dataclass, replace
from typing import Callable, Generic, Optional, ParamSpec, TypeVar

from databricks.bundles.internal._diagnostics import Diagnostics
from databricks.bundles.internal._transform import _transient_field
from databricks.bundles.jobs.functions._task_parameters import _TaskParameters
from databricks.bundles.jobs.functions.task import (
    TaskWithOutput,
    _create_task_with_output,
)
from databricks.bundles.jobs.functions.task_parameter import (
    JobParameter,
)
from databricks.bundles.jobs.internal import ast_parser
from databricks.bundles.jobs.internal.inspections import Inspections, ParameterSignature
from databricks.bundles.jobs.internal.parameters import _serialize_parameter
from databricks.bundles.jobs.models.job import Job, JobParameterDefinition
from databricks.bundles.jobs.models.job_cluster import JobCluster
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.models.tasks.run_job_task import RunJobTask
from databricks.bundles.variables import Variable, resolve_variable

R = TypeVar("R")
P = ParamSpec("P")

_T = TypeVar("_T")


class RunJobTaskWithOutput(TaskWithOutput):
    """
    Task that triggers a job and waits for its completion.
    See :type:`~databricks.bundles.jobs.models.tasks.run_job_task.RunJobTask`.
    """


@dataclass
class JobFunction(Generic[P, R], Job):
    """
    Returns :type:`~RunJobTaskWithOutput` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.
    """

    function: Callable[P, R] = _transient_field()  # type:ignore
    """
    :meta private: reserved for internal use
    """

    _diagnostics: Diagnostics = _transient_field(default_factory=Diagnostics)  # type:ignore

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> TaskWithOutput:
        base_task = _create_task_with_output(
            max_retries=None,
            min_retry_interval_millis=None,
            retry_on_timeout=None,
            email_notifications=None,
            webhook_notifications=None,
            notification_settings=None,
            timeout_seconds=None,
        )
        base_task = replace(
            base_task,
            run_job_task=RunJobTask.create(
                job_id=Variable(
                    path=f"resources.jobs.{self.resource_name}.id",
                    type=int,
                )
            ),
        )

        task_parameters = _TaskParameters.parse_call(self.function, args, kwargs)

        return task_parameters.inject(base_task)

    @property
    def tasks(self) -> Optional[list[Task]]:
        """
        Returns tasks by interpreting the annotated function.
        """

        if self._tasks:
            return self._tasks

        parameter_signature = Inspections.get_parameter_signatures(self.function)

        local_vars = {
            name: JobParameter(
                name=name, value_type=sig.tpe, default_value=sig.default_value
            )
            for name, sig in parameter_signature.items()
        }

        # FIXME resolving wouldn't allow specifying job_clusters as variables
        # as well job_cluster_key outside of @resource_generator blocks
        resolved_job_clusters = [
            resolve_variable(job_cluster)
            for job_cluster in resolve_variable(self.job_clusters)
        ]

        resolved_environments = [
            resolve_variable(environment)
            for environment in resolve_variable(self.environments)
        ]

        default_job_clusters = [
            job_cluster
            for job_cluster in resolved_job_clusters
            if resolve_variable(job_cluster.job_cluster_key) == JobCluster.DEFAULT_KEY
        ]

        if default_job_clusters:
            # FIXME check exactly one
            default_job_cluster = default_job_clusters[0]
        else:
            default_job_cluster = None

        scope = ast_parser.Scope(
            default_job_cluster=default_job_cluster,
            job_clusters=resolved_job_clusters,
            environments=resolved_environments,
            closure_vars=Inspections.get_closure_vars(self.function),
            nonlocals=Inspections.get_closure_nonlocal_vars(self.function),
            local_vars=local_vars,
            tasks={},
            automatic_task_key=None,
            source_lines=[],
            diagnostics=self._diagnostics,
            condition=None,
            file=None,
            start_line_no=None,
        )

        self._tasks = ast_parser.eval_job_func(self.function, scope)
        self._diagnostics = scope.diagnostics

        return self._tasks

    # FIXME overriding attribute with property is not safe.
    # More info: https://github.com/microsoft/pyright/issues/3646
    @tasks.setter
    def tasks(self, value):  # pyright: ignore[reportIncompatibleVariableOverride]
        self._tasks = value

    @classmethod
    def from_job_function(cls, function: Callable[P, R]) -> "JobFunction[P, R]":
        """
        :meta private: reserved for internal use
        """

        def to_parameter(
            value_key, signature: ParameterSignature
        ) -> JobParameterDefinition:
            if not signature.has_default_value:
                raise ValueError(
                    f"Job-level parameter '{value_key}' is missing a default value"
                )

            return JobParameterDefinition(
                name=value_key,
                default=_serialize_parameter(signature.tpe, signature.default_value),
            )

        name = Inspections.get_full_name(function)
        parameters = [
            to_parameter(value_key, param_sig)
            for value_key, param_sig in Inspections.get_parameter_signatures(
                function
            ).items()
        ]

        resource_name = Inspections.get_resource_name(function)

        description = Inspections.get_docstring(function)

        return cls(
            name=name,
            description=description,
            _diagnostics=Diagnostics(),
            resource_name=resource_name,
            parameters=[*parameters],  # copy to help type inference
            function=function,
        )


# TODO hide into helper
del JobFunction.__dataclass_fields__["tasks"]
