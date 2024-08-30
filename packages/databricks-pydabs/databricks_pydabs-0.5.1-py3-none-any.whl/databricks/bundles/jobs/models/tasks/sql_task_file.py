from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTaskFile", "SqlTaskFileParam"]


@dataclass(kw_only=True)
class SqlTaskFile:
    """"""

    path: VariableOr[str]
    """
    Path of the SQL file. Must be relative if the source is a remote Git repository and absolute for workspace paths.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        path: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskFileDict(TypedDict, total=False):
    """"""

    path: VariableOr[str]
    """
    Path of the SQL file. Must be relative if the source is a remote Git repository and absolute for workspace paths.
    """


SqlTaskFileParam = SqlTaskFileDict | SqlTaskFile
