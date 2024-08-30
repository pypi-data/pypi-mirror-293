from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["ClientsTypes", "ClientsTypesParam"]


@dataclass(kw_only=True)
class ClientsTypes:
    """"""

    notebooks: VariableOrOptional[bool] = None
    """
    With notebooks set, this cluster can be used for notebooks
    """

    jobs: VariableOrOptional[bool] = None
    """
    With jobs set, the cluster can be used for jobs
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        notebooks: VariableOrOptional[bool] = None,
        jobs: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class ClientsTypesDict(TypedDict, total=False):
    """"""

    notebooks: VariableOrOptional[bool]
    """
    With notebooks set, this cluster can be used for notebooks
    """

    jobs: VariableOrOptional[bool]
    """
    With jobs set, the cluster can be used for jobs
    """


ClientsTypesParam = ClientsTypesDict | ClientsTypes
