from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SparkPythonTask", "SparkPythonTaskParam"]


@dataclass(kw_only=True)
class SparkPythonTask:
    """"""

    python_file: VariableOr[str]
    """
    The Python file to be executed. Cloud file URIs (such as dbfs:/, s3:/, adls:/, gcs:/) and workspace paths are supported. For python files stored in the Databricks workspace, the path must be absolute and begin with `/`. For files stored in a remote repository, the path must be relative. This field is required.
    """

    parameters: VariableOrList[str] = field(default_factory=list)
    """
    Command line parameters passed to the Python file.
    
    Use [Task parameter variables](https://docs.databricks.com/jobs.html#parameter-variables) to set parameters containing information about job runs.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        python_file: VariableOr[str],
        parameters: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SparkPythonTaskDict(TypedDict, total=False):
    """"""

    python_file: VariableOr[str]
    """
    The Python file to be executed. Cloud file URIs (such as dbfs:/, s3:/, adls:/, gcs:/) and workspace paths are supported. For python files stored in the Databricks workspace, the path must be absolute and begin with `/`. For files stored in a remote repository, the path must be relative. This field is required.
    """

    parameters: VariableOrList[str]
    """
    Command line parameters passed to the Python file.
    
    Use [Task parameter variables](https://docs.databricks.com/jobs.html#parameter-variables) to set parameters containing information about job runs.
    """


SparkPythonTaskParam = SparkPythonTaskDict | SparkPythonTask
