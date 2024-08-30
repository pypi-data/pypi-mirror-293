from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["DbtTask", "DbtTaskParam"]


@dataclass(kw_only=True)
class DbtTask:
    """"""

    commands: VariableOrList[str]
    """
    A list of dbt commands to execute. All commands must start with `dbt`. This parameter must not be empty. A maximum of up to 10 commands can be provided.
    """

    project_directory: VariableOrOptional[str] = None
    """
    Path to the project directory. Optional for Git sourced tasks, in which
    case if no value is provided, the root of the Git repository is used.
    """

    schema: VariableOrOptional[str] = None
    """
    Optional schema to write to. This parameter is only used when a warehouse_id is also provided. If not provided, the `default` schema is used.
    """

    warehouse_id: VariableOrOptional[str] = None
    """
    ID of the SQL warehouse to connect to. If provided, we automatically generate and provide the profile and connection details to dbt. It can be overridden on a per-command basis by using the `--profiles-dir` command line argument.
    """

    profiles_directory: VariableOrOptional[str] = None
    """
    Optional (relative) path to the profiles directory. Can only be specified if no warehouse_id is specified. If no warehouse_id is specified and this folder is unset, the root directory is used.
    """

    catalog: VariableOrOptional[str] = None
    """
    Optional name of the catalog to use. The value is the top level in the 3-level namespace of Unity Catalog (catalog / schema / relation). The catalog value can only be specified if a warehouse_id is specified. Requires dbt-databricks >= 1.1.1.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        commands: VariableOrList[str],
        project_directory: VariableOrOptional[str] = None,
        schema: VariableOrOptional[str] = None,
        warehouse_id: VariableOrOptional[str] = None,
        profiles_directory: VariableOrOptional[str] = None,
        catalog: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class DbtTaskDict(TypedDict, total=False):
    """"""

    commands: VariableOrList[str]
    """
    A list of dbt commands to execute. All commands must start with `dbt`. This parameter must not be empty. A maximum of up to 10 commands can be provided.
    """

    project_directory: VariableOrOptional[str]
    """
    Path to the project directory. Optional for Git sourced tasks, in which
    case if no value is provided, the root of the Git repository is used.
    """

    schema: VariableOrOptional[str]
    """
    Optional schema to write to. This parameter is only used when a warehouse_id is also provided. If not provided, the `default` schema is used.
    """

    warehouse_id: VariableOrOptional[str]
    """
    ID of the SQL warehouse to connect to. If provided, we automatically generate and provide the profile and connection details to dbt. It can be overridden on a per-command basis by using the `--profiles-dir` command line argument.
    """

    profiles_directory: VariableOrOptional[str]
    """
    Optional (relative) path to the profiles directory. Can only be specified if no warehouse_id is specified. If no warehouse_id is specified and this folder is unset, the root directory is used.
    """

    catalog: VariableOrOptional[str]
    """
    Optional name of the catalog to use. The value is the top level in the 3-level namespace of Unity Catalog (catalog / schema / relation). The catalog value can only be specified if a warehouse_id is specified. Requires dbt-databricks >= 1.1.1.
    """


DbtTaskParam = DbtTaskDict | DbtTask
