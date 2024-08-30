from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["JobParameterDefinition", "JobParameterDefinitionParam"]


@dataclass(kw_only=True)
class JobParameterDefinition:
    """"""

    name: VariableOr[str]
    """
    The name of the defined parameter. May only contain alphanumeric characters, `_`, `-`, and `.`
    """

    default: VariableOr[str]
    """
    Default value of the parameter.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        name: VariableOr[str],
        default: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class JobParameterDefinitionDict(TypedDict, total=False):
    """"""

    name: VariableOr[str]
    """
    The name of the defined parameter. May only contain alphanumeric characters, `_`, `-`, and `.`
    """

    default: VariableOr[str]
    """
    Default value of the parameter.
    """


JobParameterDefinitionParam = JobParameterDefinitionDict | JobParameterDefinition
