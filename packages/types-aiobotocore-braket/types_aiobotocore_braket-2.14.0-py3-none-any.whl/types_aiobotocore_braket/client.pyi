"""
Type annotations for braket service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_braket.client import BraketClient

    session = get_session()
    async with session.create_client("braket") as client:
        client: BraketClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import SearchDevicesPaginator, SearchJobsPaginator, SearchQuantumTasksPaginator
from .type_defs import (
    AlgorithmSpecificationTypeDef,
    AssociationTypeDef,
    CancelJobResponseTypeDef,
    CancelQuantumTaskResponseTypeDef,
    CreateJobResponseTypeDef,
    CreateQuantumTaskResponseTypeDef,
    DeviceConfigTypeDef,
    GetDeviceResponseTypeDef,
    GetJobResponseTypeDef,
    GetQuantumTaskResponseTypeDef,
    InputFileConfigTypeDef,
    InstanceConfigTypeDef,
    JobCheckpointConfigTypeDef,
    JobOutputDataConfigTypeDef,
    JobStoppingConditionTypeDef,
    ListTagsForResourceResponseTypeDef,
    SearchDevicesFilterTypeDef,
    SearchDevicesResponseTypeDef,
    SearchJobsFilterTypeDef,
    SearchJobsResponseTypeDef,
    SearchQuantumTasksFilterTypeDef,
    SearchQuantumTasksResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("BraketClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DeviceOfflineException: Type[BotocoreClientError]
    DeviceRetiredException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class BraketClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BraketClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#can_paginate)
        """

    async def cancel_job(self, *, jobArn: str) -> CancelJobResponseTypeDef:
        """
        Cancels an Amazon Braket job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.cancel_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#cancel_job)
        """

    async def cancel_quantum_task(
        self, *, clientToken: str, quantumTaskArn: str
    ) -> CancelQuantumTaskResponseTypeDef:
        """
        Cancels the specified task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.cancel_quantum_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#cancel_quantum_task)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#close)
        """

    async def create_job(
        self,
        *,
        algorithmSpecification: AlgorithmSpecificationTypeDef,
        clientToken: str,
        deviceConfig: DeviceConfigTypeDef,
        instanceConfig: InstanceConfigTypeDef,
        jobName: str,
        outputDataConfig: JobOutputDataConfigTypeDef,
        roleArn: str,
        associations: Sequence[AssociationTypeDef] = ...,
        checkpointConfig: JobCheckpointConfigTypeDef = ...,
        hyperParameters: Mapping[str, str] = ...,
        inputDataConfig: Sequence[InputFileConfigTypeDef] = ...,
        stoppingCondition: JobStoppingConditionTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateJobResponseTypeDef:
        """
        Creates an Amazon Braket job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#create_job)
        """

    async def create_quantum_task(
        self,
        *,
        action: str,
        clientToken: str,
        deviceArn: str,
        outputS3Bucket: str,
        outputS3KeyPrefix: str,
        shots: int,
        associations: Sequence[AssociationTypeDef] = ...,
        deviceParameters: str = ...,
        jobToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateQuantumTaskResponseTypeDef:
        """
        Creates a quantum task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.create_quantum_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#create_quantum_task)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#generate_presigned_url)
        """

    async def get_device(self, *, deviceArn: str) -> GetDeviceResponseTypeDef:
        """
        Retrieves the devices available in Amazon Braket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_device)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_device)
        """

    async def get_job(
        self, *, jobArn: str, additionalAttributeNames: Sequence[Literal["QueueInfo"]] = ...
    ) -> GetJobResponseTypeDef:
        """
        Retrieves the specified Amazon Braket job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_job)
        """

    async def get_quantum_task(
        self, *, quantumTaskArn: str, additionalAttributeNames: Sequence[Literal["QueueInfo"]] = ...
    ) -> GetQuantumTaskResponseTypeDef:
        """
        Retrieves the specified quantum task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_quantum_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_quantum_task)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Shows the tags associated with this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#list_tags_for_resource)
        """

    async def search_devices(
        self,
        *,
        filters: Sequence[SearchDevicesFilterTypeDef],
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> SearchDevicesResponseTypeDef:
        """
        Searches for devices using the specified filters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.search_devices)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#search_devices)
        """

    async def search_jobs(
        self,
        *,
        filters: Sequence[SearchJobsFilterTypeDef],
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> SearchJobsResponseTypeDef:
        """
        Searches for Amazon Braket jobs that match the specified filter values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.search_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#search_jobs)
        """

    async def search_quantum_tasks(
        self,
        *,
        filters: Sequence[SearchQuantumTasksFilterTypeDef],
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> SearchQuantumTasksResponseTypeDef:
        """
        Searches for tasks that match the specified filter values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.search_quantum_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#search_quantum_tasks)
        """

    async def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Add a tag to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#tag_resource)
        """

    async def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Remove tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#untag_resource)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_devices"]) -> SearchDevicesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["search_jobs"]) -> SearchJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_quantum_tasks"]
    ) -> SearchQuantumTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/#get_paginator)
        """

    async def __aenter__(self) -> "BraketClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/braket.html#Braket.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_braket/client/)
        """
