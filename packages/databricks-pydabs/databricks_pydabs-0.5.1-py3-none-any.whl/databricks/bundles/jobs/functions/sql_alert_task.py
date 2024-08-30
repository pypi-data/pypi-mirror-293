from dataclasses import dataclass
from enum import Enum

from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput

__all__ = [
    "AlertState",
    "SqlAlertTaskFunction",
    "SqlAlertTaskOutput",
]


class AlertState(Enum):
    """
    The state of the SQL alert.

    - UNKNOWN: alert yet to be evaluated
    - OK: alert evaluated and did not fulfill trigger conditions
    - TRIGGERED: alert evaluated and fulfilled trigger conditions
    """

    UNKNOWN = "UNKNOWN"
    OK = "OK"
    TRIGGERED = "TRIGGERED"


@dataclass(kw_only=True)
class SqlAlertTaskOutput:
    alert_state: AlertState


class SqlAlertTaskWithOutput(TaskWithOutput):
    @property
    def output(self) -> SqlAlertTaskOutput:
        raise Exception(
            "Accessing task output outside of @job decorator isn't supported"
        )


class SqlAlertTaskFunction(TaskFunction[[], None]):
    base_task: SqlAlertTaskWithOutput

    def __call__(self) -> SqlAlertTaskWithOutput:
        return super().__call__()  # type:ignore
