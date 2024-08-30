from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.compute.models.adlsgen2_info import (
    Adlsgen2Info,
    Adlsgen2InfoParam,
)
from databricks.bundles.compute.models.dbfs_storage_info import (
    DbfsStorageInfo,
    DbfsStorageInfoParam,
)
from databricks.bundles.compute.models.gcs_storage_info import (
    GcsStorageInfo,
    GcsStorageInfoParam,
)
from databricks.bundles.compute.models.local_file_info import (
    LocalFileInfo,
    LocalFileInfoParam,
)
from databricks.bundles.compute.models.s3_storage_info import (
    S3StorageInfo,
    S3StorageInfoParam,
)
from databricks.bundles.compute.models.volumes_storage_info import (
    VolumesStorageInfo,
    VolumesStorageInfoParam,
)
from databricks.bundles.compute.models.workspace_storage_info import (
    WorkspaceStorageInfo,
    WorkspaceStorageInfoParam,
)
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["InitScriptInfo", "InitScriptInfoParam"]


@dataclass(kw_only=True)
class InitScriptInfo:
    """"""

    workspace: VariableOrOptional[WorkspaceStorageInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "workspace" : { "destination" : "/Users/user1@databricks.com/my-init.sh" } }`
    """

    volumes: VariableOrOptional[VolumesStorageInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "volumes" : { "destination" : "/Volumes/my-init.sh" } }`
    """

    s3: VariableOrOptional[S3StorageInfo] = None
    """
    destination and either the region or endpoint need to be provided. e.g.
    `{ "s3": { "destination" : "s3://cluster_log_bucket/prefix", "region" : "us-west-2" } }`
    Cluster iam role is used to access s3, please make sure the cluster iam role in
    `instance_profile_arn` has permission to write data to the s3 destination.
    """

    file: VariableOrOptional[LocalFileInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "file" : { "destination" : "file:/my/local/file.sh" } }`
    """

    dbfs: VariableOrOptional[DbfsStorageInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "dbfs" : { "destination" : "dbfs:/home/cluster_log" } }`
    """

    abfss: VariableOrOptional[Adlsgen2Info] = None
    """
    destination needs to be provided. e.g.
    `{ "abfss" : { "destination" : "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>" } }`
    """

    gcs: VariableOrOptional[GcsStorageInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "gcs": { "destination": "gs://my-bucket/file.sh" } }`
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        workspace: VariableOrOptional[WorkspaceStorageInfoParam] = None,
        volumes: VariableOrOptional[VolumesStorageInfoParam] = None,
        s3: VariableOrOptional[S3StorageInfoParam] = None,
        file: VariableOrOptional[LocalFileInfoParam] = None,
        dbfs: VariableOrOptional[DbfsStorageInfoParam] = None,
        abfss: VariableOrOptional[Adlsgen2InfoParam] = None,
        gcs: VariableOrOptional[GcsStorageInfoParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class InitScriptInfoDict(TypedDict, total=False):
    """"""

    workspace: VariableOrOptional[WorkspaceStorageInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "workspace" : { "destination" : "/Users/user1@databricks.com/my-init.sh" } }`
    """

    volumes: VariableOrOptional[VolumesStorageInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "volumes" : { "destination" : "/Volumes/my-init.sh" } }`
    """

    s3: VariableOrOptional[S3StorageInfoParam]
    """
    destination and either the region or endpoint need to be provided. e.g.
    `{ "s3": { "destination" : "s3://cluster_log_bucket/prefix", "region" : "us-west-2" } }`
    Cluster iam role is used to access s3, please make sure the cluster iam role in
    `instance_profile_arn` has permission to write data to the s3 destination.
    """

    file: VariableOrOptional[LocalFileInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "file" : { "destination" : "file:/my/local/file.sh" } }`
    """

    dbfs: VariableOrOptional[DbfsStorageInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "dbfs" : { "destination" : "dbfs:/home/cluster_log" } }`
    """

    abfss: VariableOrOptional[Adlsgen2InfoParam]
    """
    destination needs to be provided. e.g.
    `{ "abfss" : { "destination" : "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>" } }
    """

    gcs: VariableOrOptional[GcsStorageInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "gcs": { "destination": "gs://my-bucket/file.sh" } }`
    """


InitScriptInfoParam = InitScriptInfoDict | InitScriptInfo
