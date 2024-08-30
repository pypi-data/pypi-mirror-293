import dataclasses
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, ParamSpec, TypeVar

from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "ComputeTask",
    "ComputeTaskFunction",
]

R = TypeVar("R")
P = ParamSpec("P")


@dataclass(kw_only=True)
class ComputeTask(Generic[R], TaskWithOutput):
    """
    Compute tasks are tasks running on existing clusters, job clusters, or serverless
    compute.
    """

    class TaskValues:
        """
        Task values are used to share information between tasks.

        In this example, `first_task` sets value for key `my_value` and `second_task` reads it.

        .. code-block:: python

            @task
            def first_task():
                dbutils.jobs.taskValues.set("my_value", 42)

            @task
            def second_task(value: int):
                print(value)

            def my_job():
                first = first_task()

                second_task(first.values.my_value)

        See `Share information between tasks in a Databricks job
        <https://docs.databricks.com/en/jobs/share-task-context.html>`_
        """

        def __getattribute__(self, item) -> Any:
            pass

    def with_existing_cluster_id(self, value: str) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.existing_cluster_id` with a new value
        """

        return dataclasses.replace(self, existing_cluster_id=value)

    def with_job_cluster_key(self, value: str) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.job_cluster_key` with a new value
        """

        return dataclasses.replace(self, job_cluster_key=value)

    def with_environment_key(self, value: str) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.environment_key` with a new value
        """

        return dataclasses.replace(self, environment_key=value)

    @property
    def values(self) -> TaskValues:
        """
        Access values set by this task. See :class:`TaskValues` for more information.
        """

        raise Exception(
            "Accessing task values outside of @job decorator isn't supported"
        )

    @property
    def result(self) -> R:
        """
        Returns task result. For functions decorated with
        :func:`@task <databricks.bundles.jobs.task>`, it's their return value.
        """

        raise Exception(
            "Accessing task result outside of @job decorator isn't supported"
        )

    @property
    def output(self) -> R:
        """
        Returns task output.

        Deprecated: use :attr:`~result` instead
        """

        raise Exception(
            "Accessing task output outside of @job decorator isn't supported"
        )


@dataclass(kw_only=True, frozen=True)
class ComputeTaskFunction(TaskFunction[P, R]):
    """
    Returns :class:`ComputeTask` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.
    """

    base_task: ComputeTask[R]

    def __call__(self, /, *args: P.args, **kwargs: P.kwargs) -> ComputeTask[R]:
        return super().__call__(*args, **kwargs)  # type:ignore
