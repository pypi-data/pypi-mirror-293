from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.cron_schedule import CronSchedule, CronScheduleParam
from databricks.bundles.jobs.models.email_notifications import (
    EmailNotifications,
    EmailNotificationsParam,
    JobNotificationSettings,
    JobNotificationSettingsParam,
)
from databricks.bundles.jobs.models.job_cluster import JobCluster, JobClusterParam
from databricks.bundles.jobs.models.job_environment import (
    JobEnvironment,
    JobEnvironmentParam,
)
from databricks.bundles.jobs.models.job_parameter import (
    JobParameterDefinition,
    JobParameterDefinitionParam,
)
from databricks.bundles.jobs.models.permission import Permission, PermissionParam
from databricks.bundles.jobs.models.queue_settings import (
    QueueSettings,
    QueueSettingsParam,
)
from databricks.bundles.jobs.models.run_as import RunAs, RunAsParam
from databricks.bundles.jobs.models.task import Task, TaskParam
from databricks.bundles.jobs.models.trigger import TriggerSettings, TriggerSettingsParam
from databricks.bundles.jobs.models.webhook_notifications import (
    WebhookNotifications,
    WebhookNotificationsParam,
)
from databricks.bundles.resource import Resource
from databricks.bundles.variables import (
    VariableOrDict,
    VariableOrList,
    VariableOrOptional,
)

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["Job", "JobParam"]


@dataclass(kw_only=True)
class Job(Resource):
    """"""

    name: VariableOrOptional[str] = None
    """
    An optional name for the job. The maximum length is 4096 bytes in UTF-8 encoding.
    """

    description: VariableOrOptional[str] = None
    """
    An optional description for the job. The maximum length is 1024 characters in UTF-8 encoding.
    """

    email_notifications: VariableOrOptional[EmailNotifications] = None
    """
    An optional set of email addresses that is notified when runs of this job begin or complete as well as when this job is deleted.
    """

    webhook_notifications: VariableOrOptional[WebhookNotifications] = None
    """
    A collection of system notification IDs to notify when runs of this job begin or complete.
    """

    notification_settings: VariableOrOptional[JobNotificationSettings] = None
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this job.
    """

    timeout_seconds: VariableOrOptional[int] = None
    """
    An optional timeout applied to each run of this job. A value of `0` means no timeout.
    """

    schedule: VariableOrOptional[CronSchedule] = None
    """
    An optional periodic schedule for this job. The default behavior is that the job only runs when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    trigger: VariableOrOptional[TriggerSettings] = None
    """
    A configuration to trigger a run when certain conditions are met. The default behavior is that the job runs only when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    max_concurrent_runs: VariableOrOptional[int] = None
    """
    An optional maximum allowed number of concurrent runs of the job.
    Set this value if you want to be able to execute multiple runs of the same job concurrently.
    This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters.
    This setting affects only new runs. For example, suppose the job’s concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won’t kill any of the active runs.
    However, from then on, new runs are skipped unless there are fewer than 3 active runs.
    This value cannot exceed 1000. Setting this value to `0` causes all new runs to be skipped.
    """

    tasks: VariableOrList[Task] = field(default_factory=list)
    """
    A list of task specifications to be executed by this job.
    """

    job_clusters: VariableOrList[JobCluster] = field(default_factory=list)
    """
    A list of job cluster specifications that can be shared and reused by tasks of this job. Libraries cannot be declared in a shared job cluster. You must declare dependent libraries in task settings.
    """

    tags: VariableOrDict[str] = field(default_factory=dict)
    """
    A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
    """

    queue: VariableOrOptional[QueueSettings] = None
    """
    The queue settings of the job.
    """

    parameters: VariableOrList[JobParameterDefinition] = field(default_factory=list)
    """
    Job-level parameter definitions
    """

    run_as: VariableOrOptional[RunAs] = None

    environments: VariableOrList[JobEnvironment] = field(default_factory=list)
    """
    A list of task execution environment specifications that can be referenced by tasks of this job.
    """

    permissions: VariableOrList[Permission] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        /,
        *,
        resource_name: str,
        name: VariableOrOptional[str] = None,
        description: VariableOrOptional[str] = None,
        email_notifications: VariableOrOptional[EmailNotificationsParam] = None,
        webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
        notification_settings: VariableOrOptional[JobNotificationSettingsParam] = None,
        timeout_seconds: VariableOrOptional[int] = None,
        schedule: VariableOrOptional[CronScheduleParam] = None,
        trigger: VariableOrOptional[TriggerSettingsParam] = None,
        max_concurrent_runs: VariableOrOptional[int] = None,
        tasks: Optional[VariableOrList[TaskParam]] = None,
        job_clusters: Optional[VariableOrList[JobClusterParam]] = None,
        tags: Optional[VariableOrDict[str]] = None,
        queue: VariableOrOptional[QueueSettingsParam] = None,
        parameters: Optional[VariableOrList[JobParameterDefinitionParam]] = None,
        run_as: VariableOrOptional[RunAsParam] = None,
        environments: Optional[VariableOrList[JobEnvironmentParam]] = None,
        permissions: Optional[VariableOrList[PermissionParam]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobDict(TypedDict, total=False):
    """"""

    name: VariableOrOptional[str]
    """
    An optional name for the job. The maximum length is 4096 bytes in UTF-8 encoding.
    """

    description: VariableOrOptional[str]
    """
    An optional description for the job. The maximum length is 1024 characters in UTF-8 encoding.
    """

    email_notifications: VariableOrOptional[EmailNotificationsParam]
    """
    An optional set of email addresses that is notified when runs of this job begin or complete as well as when this job is deleted.
    """

    webhook_notifications: VariableOrOptional[WebhookNotificationsParam]
    """
    A collection of system notification IDs to notify when runs of this job begin or complete.
    """

    notification_settings: VariableOrOptional[JobNotificationSettingsParam]
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this job.
    """

    timeout_seconds: VariableOrOptional[int]
    """
    An optional timeout applied to each run of this job. A value of `0` means no timeout.
    """

    schedule: VariableOrOptional[CronScheduleParam]
    """
    An optional periodic schedule for this job. The default behavior is that the job only runs when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    trigger: VariableOrOptional[TriggerSettingsParam]
    """
    A configuration to trigger a run when certain conditions are met. The default behavior is that the job runs only when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    max_concurrent_runs: VariableOrOptional[int]
    """
    An optional maximum allowed number of concurrent runs of the job.
    Set this value if you want to be able to execute multiple runs of the same job concurrently.
    This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters.
    This setting affects only new runs. For example, suppose the job’s concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won’t kill any of the active runs.
    However, from then on, new runs are skipped unless there are fewer than 3 active runs.
    This value cannot exceed 1000. Setting this value to `0` causes all new runs to be skipped.
    """

    tasks: VariableOrList[TaskParam]
    """
    A list of task specifications to be executed by this job.
    """

    job_clusters: VariableOrList[JobClusterParam]
    """
    A list of job cluster specifications that can be shared and reused by tasks of this job. Libraries cannot be declared in a shared job cluster. You must declare dependent libraries in task settings.
    """

    tags: VariableOrDict[str]
    """
    A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
    """

    queue: VariableOrOptional[QueueSettingsParam]
    """
    The queue settings of the job.
    """

    parameters: VariableOrList[JobParameterDefinitionParam]
    """
    Job-level parameter definitions
    """

    run_as: VariableOrOptional[RunAsParam]

    environments: VariableOrList[JobEnvironmentParam]
    """
    A list of task execution environment specifications that can be referenced by tasks of this job.
    """

    permissions: VariableOrList[PermissionParam]


JobParam = JobDict | Job
