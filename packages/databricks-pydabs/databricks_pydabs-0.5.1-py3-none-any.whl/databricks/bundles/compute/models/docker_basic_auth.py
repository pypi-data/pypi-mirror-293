from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["DockerBasicAuth", "DockerBasicAuthParam"]


@dataclass(kw_only=True)
class DockerBasicAuth:
    """"""

    username: VariableOrOptional[str] = None
    """
    Name of the user
    """

    password: VariableOrOptional[str] = None
    """
    Password of the user
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        username: VariableOrOptional[str] = None,
        password: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class DockerBasicAuthDict(TypedDict, total=False):
    """"""

    username: VariableOrOptional[str]
    """
    Name of the user
    """

    password: VariableOrOptional[str]
    """
    Password of the user
    """


DockerBasicAuthParam = DockerBasicAuthDict | DockerBasicAuth
