from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["S3StorageInfo", "S3StorageInfoParam"]


@dataclass(kw_only=True)
class S3StorageInfo:
    """"""

    destination: VariableOr[str]
    """
    S3 destination, e.g. `s3://my-bucket/some-prefix` Note that logs will be delivered using
    cluster iam role, please make sure you set cluster iam role and the role has write access to the
    destination. Please also note that you cannot use AWS keys to deliver logs.
    """

    region: VariableOrOptional[str] = None
    """
    S3 region, e.g. `us-west-2`. Either region or endpoint needs to be set. If both are set,
    endpoint will be used.
    """

    endpoint: VariableOrOptional[str] = None
    """
    S3 endpoint, e.g. `https://s3-us-west-2.amazonaws.com`. Either region or endpoint needs to be set.
    If both are set, endpoint will be used.
    """

    enable_encryption: VariableOrOptional[bool] = None
    """
    (Optional) Flag to enable server side encryption, `false` by default.
    """

    encryption_type: VariableOrOptional[str] = None
    """
    (Optional) The encryption type, it could be `sse-s3` or `sse-kms`. It will be used only when
    encryption is enabled and the default type is `sse-s3`.
    """

    kms_key: VariableOrOptional[str] = None
    """
    (Optional) Kms key which will be used if encryption is enabled and encryption type is set to `sse-kms`.
    """

    canned_acl: VariableOrOptional[str] = None
    """
    (Optional) Set canned access control list for the logs, e.g. `bucket-owner-full-control`.
    If `canned_cal` is set, please make sure the cluster iam role has `s3:PutObjectAcl` permission on
    the destination bucket and prefix. The full list of possible canned acl can be found at
    http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl.
    Please also note that by default only the object owner gets full controls. If you are using cross account
    role for writing data, you may want to set `bucket-owner-full-control` to make bucket owner able to
    read the logs.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        destination: VariableOr[str],
        region: VariableOrOptional[str] = None,
        endpoint: VariableOrOptional[str] = None,
        enable_encryption: VariableOrOptional[bool] = None,
        encryption_type: VariableOrOptional[str] = None,
        kms_key: VariableOrOptional[str] = None,
        canned_acl: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class S3StorageInfoDict(TypedDict, total=False):
    """"""

    destination: VariableOr[str]
    """
    S3 destination, e.g. `s3://my-bucket/some-prefix` Note that logs will be delivered using
    cluster iam role, please make sure you set cluster iam role and the role has write access to the
    destination. Please also note that you cannot use AWS keys to deliver logs.
    """

    region: VariableOrOptional[str]
    """
    S3 region, e.g. `us-west-2`. Either region or endpoint needs to be set. If both are set,
    endpoint will be used.
    """

    endpoint: VariableOrOptional[str]
    """
    S3 endpoint, e.g. `https://s3-us-west-2.amazonaws.com`. Either region or endpoint needs to be set.
    If both are set, endpoint will be used.
    """

    enable_encryption: VariableOrOptional[bool]
    """
    (Optional) Flag to enable server side encryption, `false` by default.
    """

    encryption_type: VariableOrOptional[str]
    """
    (Optional) The encryption type, it could be `sse-s3` or `sse-kms`. It will be used only when
    encryption is enabled and the default type is `sse-s3`.
    """

    kms_key: VariableOrOptional[str]
    """
    (Optional) Kms key which will be used if encryption is enabled and encryption type is set to `sse-kms`.
    """

    canned_acl: VariableOrOptional[str]
    """
    (Optional) Set canned access control list for the logs, e.g. `bucket-owner-full-control`.
    If `canned_cal` is set, please make sure the cluster iam role has `s3:PutObjectAcl` permission on
    the destination bucket and prefix. The full list of possible canned acl can be found at
    http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl.
    Please also note that by default only the object owner gets full controls. If you are using cross account
    role for writing data, you may want to set `bucket-owner-full-control` to make bucket owner able to
    read the logs.
    """


S3StorageInfoParam = S3StorageInfoDict | S3StorageInfo
