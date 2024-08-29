"""
Type annotations for pcs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_pcs.client import ParallelComputingServiceClient

    session = Session()
    client: ParallelComputingServiceClient = session.client("pcs")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import PurchaseOptionType, SizeType
from .paginator import ListClustersPaginator, ListComputeNodeGroupsPaginator, ListQueuesPaginator
from .type_defs import (
    ClusterSlurmConfigurationRequestTypeDef,
    ComputeNodeGroupConfigurationTypeDef,
    ComputeNodeGroupSlurmConfigurationRequestTypeDef,
    CreateClusterResponseTypeDef,
    CreateComputeNodeGroupResponseTypeDef,
    CreateQueueResponseTypeDef,
    CustomLaunchTemplateTypeDef,
    EmptyResponseMetadataTypeDef,
    GetClusterResponseTypeDef,
    GetComputeNodeGroupResponseTypeDef,
    GetQueueResponseTypeDef,
    InstanceConfigTypeDef,
    ListClustersResponseTypeDef,
    ListComputeNodeGroupsResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NetworkingRequestTypeDef,
    RegisterComputeNodeGroupInstanceResponseTypeDef,
    ScalingConfigurationRequestTypeDef,
    SchedulerRequestTypeDef,
    SpotOptionsTypeDef,
    UpdateComputeNodeGroupResponseTypeDef,
    UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef,
    UpdateQueueResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ParallelComputingServiceClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ParallelComputingServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ParallelComputingServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#close)
        """

    def create_cluster(
        self,
        *,
        clusterName: str,
        scheduler: SchedulerRequestTypeDef,
        size: SizeType,
        networking: NetworkingRequestTypeDef,
        slurmConfiguration: ClusterSlurmConfigurationRequestTypeDef = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateClusterResponseTypeDef:
        """
        Creates a cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#create_cluster)
        """

    def create_compute_node_group(
        self,
        *,
        clusterIdentifier: str,
        computeNodeGroupName: str,
        subnetIds: Sequence[str],
        customLaunchTemplate: CustomLaunchTemplateTypeDef,
        iamInstanceProfileArn: str,
        scalingConfiguration: ScalingConfigurationRequestTypeDef,
        instanceConfigs: Sequence[InstanceConfigTypeDef],
        amiId: str = ...,
        purchaseOption: PurchaseOptionType = ...,
        spotOptions: SpotOptionsTypeDef = ...,
        slurmConfiguration: ComputeNodeGroupSlurmConfigurationRequestTypeDef = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateComputeNodeGroupResponseTypeDef:
        """
        Creates a managed set of compute nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_compute_node_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#create_compute_node_group)
        """

    def create_queue(
        self,
        *,
        clusterIdentifier: str,
        queueName: str,
        computeNodeGroupConfigurations: Sequence[ComputeNodeGroupConfigurationTypeDef] = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateQueueResponseTypeDef:
        """
        Creates a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.create_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#create_queue)
        """

    def delete_cluster(self, *, clusterIdentifier: str, clientToken: str = ...) -> Dict[str, Any]:
        """
        Deletes a cluster and all its linked resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#delete_cluster)
        """

    def delete_compute_node_group(
        self, *, clusterIdentifier: str, computeNodeGroupIdentifier: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_compute_node_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#delete_compute_node_group)
        """

    def delete_queue(
        self, *, clusterIdentifier: str, queueIdentifier: str, clientToken: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a job queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.delete_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#delete_queue)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#generate_presigned_url)
        """

    def get_cluster(self, *, clusterIdentifier: str) -> GetClusterResponseTypeDef:
        """
        Returns detailed information about a running cluster in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_cluster)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_cluster)
        """

    def get_compute_node_group(
        self, *, clusterIdentifier: str, computeNodeGroupIdentifier: str
    ) -> GetComputeNodeGroupResponseTypeDef:
        """
        Returns detailed information about a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_compute_node_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_compute_node_group)
        """

    def get_queue(self, *, clusterIdentifier: str, queueIdentifier: str) -> GetQueueResponseTypeDef:
        """
        Returns detailed information about a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_queue)
        """

    def list_clusters(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListClustersResponseTypeDef:
        """
        Returns a list of running clusters in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_clusters)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#list_clusters)
        """

    def list_compute_node_groups(
        self, *, clusterIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListComputeNodeGroupsResponseTypeDef:
        """
        Returns a list of all compute node groups associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_compute_node_groups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#list_compute_node_groups)
        """

    def list_queues(
        self, *, clusterIdentifier: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListQueuesResponseTypeDef:
        """
        Returns a list of all queues associated with a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_queues)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#list_queues)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of all tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#list_tags_for_resource)
        """

    def register_compute_node_group_instance(
        self, *, clusterIdentifier: str, bootstrapId: str
    ) -> RegisterComputeNodeGroupInstanceResponseTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.register_compute_node_group_instance)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#register_compute_node_group_instance)
        """

    def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or edits tags on an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#tag_resource)
        """

    def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from an Amazon Web Services PCS resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#untag_resource)
        """

    def update_compute_node_group(
        self,
        *,
        clusterIdentifier: str,
        computeNodeGroupIdentifier: str,
        amiId: str = ...,
        subnetIds: Sequence[str] = ...,
        customLaunchTemplate: CustomLaunchTemplateTypeDef = ...,
        purchaseOption: PurchaseOptionType = ...,
        spotOptions: SpotOptionsTypeDef = ...,
        scalingConfiguration: ScalingConfigurationRequestTypeDef = ...,
        iamInstanceProfileArn: str = ...,
        slurmConfiguration: UpdateComputeNodeGroupSlurmConfigurationRequestTypeDef = ...,
        clientToken: str = ...,
    ) -> UpdateComputeNodeGroupResponseTypeDef:
        """
        Updates a compute node group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.update_compute_node_group)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#update_compute_node_group)
        """

    def update_queue(
        self,
        *,
        clusterIdentifier: str,
        queueIdentifier: str,
        computeNodeGroupConfigurations: Sequence[ComputeNodeGroupConfigurationTypeDef] = ...,
        clientToken: str = ...,
    ) -> UpdateQueueResponseTypeDef:
        """
        Updates the compute node group configuration of a queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.update_queue)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#update_queue)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_clusters"]) -> ListClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_compute_node_groups"]
    ) -> ListComputeNodeGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_queues"]) -> ListQueuesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pcs.html#ParallelComputingService.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pcs/client/#get_paginator)
        """
