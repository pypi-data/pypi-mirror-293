from dataclasses import dataclass
from typing import Any, Optional, Union

__all__ = [
    "ConstantParameter",
    "TaskReferenceParameter",
    "JobParameter",
    "TaskParameter",
]

from databricks.bundles.jobs.internal.parameters import _serialize_parameter


@dataclass
class ConstantParameter:
    value: Any

    @property
    def value_type(self) -> type:
        return type(self.value)

    def serialize(self) -> str:
        return _serialize_parameter(type(self.value), self.value)


@dataclass(kw_only=True)
class TaskReferenceParameter:
    task_key: str
    path: list[str]

    def serialize(self) -> str:
        return f"{{{{tasks.{self.task_key}.{'.'.join(self.path)}}}}}"

    def __post_init__(self):
        if not self.path:
            raise ValueError("Path must not be empty")


@dataclass(kw_only=True)
class ForEachInputTaskParameter:
    attribute: Optional[str] = None

    def serialize(self) -> str:
        if self.attribute:
            return f"{{{{input.{self.attribute}}}}}"
        else:
            return "{{input}}"


@dataclass(kw_only=True)
class JobParameter:
    name: str
    value_type: type
    default_value: Any

    def __post_init__(self):
        if not isinstance(self.default_value, self.value_type):
            raise ValueError(
                f"Expected default value for parameter '{self.name}' to be {self.value_type}, "
                f"but got {type(self.default_value)}"
            )

    def serialize(self) -> str:
        return f"{{{{job.parameters.{self.name}}}}}"


TaskParameter = Union[
    ConstantParameter,
    TaskReferenceParameter,
    JobParameter,
    ForEachInputTaskParameter,
]
