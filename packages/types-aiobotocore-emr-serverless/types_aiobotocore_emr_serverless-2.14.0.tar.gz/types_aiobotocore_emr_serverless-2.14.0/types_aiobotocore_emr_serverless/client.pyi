"""
Type annotations for emr-serverless service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_emr_serverless.client import EMRServerlessClient

    session = get_session()
    async with session.create_client("emr-serverless") as client:
        client: EMRServerlessClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import ApplicationStateType, ArchitectureType, JobRunModeType, JobRunStateType
from .paginator import ListApplicationsPaginator, ListJobRunAttemptsPaginator, ListJobRunsPaginator
from .type_defs import (
    AutoStartConfigTypeDef,
    AutoStopConfigTypeDef,
    CancelJobRunResponseTypeDef,
    ConfigurationOverridesUnionTypeDef,
    ConfigurationUnionTypeDef,
    CreateApplicationResponseTypeDef,
    GetApplicationResponseTypeDef,
    GetDashboardForJobRunResponseTypeDef,
    GetJobRunResponseTypeDef,
    ImageConfigurationInputTypeDef,
    InitialCapacityConfigTypeDef,
    InteractiveConfigurationTypeDef,
    JobDriverUnionTypeDef,
    ListApplicationsResponseTypeDef,
    ListJobRunAttemptsResponseTypeDef,
    ListJobRunsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    MaximumAllowedResourcesTypeDef,
    MonitoringConfigurationUnionTypeDef,
    NetworkConfigurationUnionTypeDef,
    RetryPolicyTypeDef,
    StartJobRunResponseTypeDef,
    TimestampTypeDef,
    UpdateApplicationResponseTypeDef,
    WorkerTypeSpecificationInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("EMRServerlessClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EMRServerlessClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EMRServerlessClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#can_paginate)
        """

    async def cancel_job_run(
        self, *, applicationId: str, jobRunId: str
    ) -> CancelJobRunResponseTypeDef:
        """
        Cancels a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.cancel_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#cancel_job_run)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#close)
        """

    async def create_application(
        self,
        *,
        releaseLabel: str,
        type: str,
        clientToken: str,
        name: str = ...,
        initialCapacity: Mapping[str, InitialCapacityConfigTypeDef] = ...,
        maximumCapacity: MaximumAllowedResourcesTypeDef = ...,
        tags: Mapping[str, str] = ...,
        autoStartConfiguration: AutoStartConfigTypeDef = ...,
        autoStopConfiguration: AutoStopConfigTypeDef = ...,
        networkConfiguration: NetworkConfigurationUnionTypeDef = ...,
        architecture: ArchitectureType = ...,
        imageConfiguration: ImageConfigurationInputTypeDef = ...,
        workerTypeSpecifications: Mapping[str, WorkerTypeSpecificationInputTypeDef] = ...,
        runtimeConfiguration: Sequence[ConfigurationUnionTypeDef] = ...,
        monitoringConfiguration: MonitoringConfigurationUnionTypeDef = ...,
        interactiveConfiguration: InteractiveConfigurationTypeDef = ...,
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#create_application)
        """

    async def delete_application(self, *, applicationId: str) -> Dict[str, Any]:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#delete_application)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#generate_presigned_url)
        """

    async def get_application(self, *, applicationId: str) -> GetApplicationResponseTypeDef:
        """
        Displays detailed information about a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_application)
        """

    async def get_dashboard_for_job_run(
        self, *, applicationId: str, jobRunId: str, attempt: int = ...
    ) -> GetDashboardForJobRunResponseTypeDef:
        """
        Creates and returns a URL that you can use to access the application UIs for a
        job
        run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_dashboard_for_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_dashboard_for_job_run)
        """

    async def get_job_run(
        self, *, applicationId: str, jobRunId: str, attempt: int = ...
    ) -> GetJobRunResponseTypeDef:
        """
        Displays detailed information about a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_job_run)
        """

    async def list_applications(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        states: Sequence[ApplicationStateType] = ...,
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists applications based on a set of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#list_applications)
        """

    async def list_job_run_attempts(
        self, *, applicationId: str, jobRunId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListJobRunAttemptsResponseTypeDef:
        """
        Lists all attempt of a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.list_job_run_attempts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#list_job_run_attempts)
        """

    async def list_job_runs(
        self,
        *,
        applicationId: str,
        nextToken: str = ...,
        maxResults: int = ...,
        createdAtAfter: TimestampTypeDef = ...,
        createdAtBefore: TimestampTypeDef = ...,
        states: Sequence[JobRunStateType] = ...,
        mode: JobRunModeType = ...,
    ) -> ListJobRunsResponseTypeDef:
        """
        Lists job runs based on a set of parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.list_job_runs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#list_job_runs)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags assigned to the resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#list_tags_for_resource)
        """

    async def start_application(self, *, applicationId: str) -> Dict[str, Any]:
        """
        Starts a specified application and initializes initial capacity if configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.start_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#start_application)
        """

    async def start_job_run(
        self,
        *,
        applicationId: str,
        clientToken: str,
        executionRoleArn: str,
        jobDriver: JobDriverUnionTypeDef = ...,
        configurationOverrides: ConfigurationOverridesUnionTypeDef = ...,
        tags: Mapping[str, str] = ...,
        executionTimeoutMinutes: int = ...,
        name: str = ...,
        mode: JobRunModeType = ...,
        retryPolicy: RetryPolicyTypeDef = ...,
    ) -> StartJobRunResponseTypeDef:
        """
        Starts a job run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.start_job_run)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#start_job_run)
        """

    async def stop_application(self, *, applicationId: str) -> Dict[str, Any]:
        """
        Stops a specified application and releases initial capacity if configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.stop_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#stop_application)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns tags to resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#untag_resource)
        """

    async def update_application(
        self,
        *,
        applicationId: str,
        clientToken: str,
        initialCapacity: Mapping[str, InitialCapacityConfigTypeDef] = ...,
        maximumCapacity: MaximumAllowedResourcesTypeDef = ...,
        autoStartConfiguration: AutoStartConfigTypeDef = ...,
        autoStopConfiguration: AutoStopConfigTypeDef = ...,
        networkConfiguration: NetworkConfigurationUnionTypeDef = ...,
        architecture: ArchitectureType = ...,
        imageConfiguration: ImageConfigurationInputTypeDef = ...,
        workerTypeSpecifications: Mapping[str, WorkerTypeSpecificationInputTypeDef] = ...,
        interactiveConfiguration: InteractiveConfigurationTypeDef = ...,
        releaseLabel: str = ...,
        runtimeConfiguration: Sequence[ConfigurationUnionTypeDef] = ...,
        monitoringConfiguration: MonitoringConfigurationUnionTypeDef = ...,
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates a specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#update_application)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_job_run_attempts"]
    ) -> ListJobRunAttemptsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_job_runs"]) -> ListJobRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/#get_paginator)
        """

    async def __aenter__(self) -> "EMRServerlessClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-serverless.html#EMRServerless.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_serverless/client/)
        """
