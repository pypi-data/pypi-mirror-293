"""
Type annotations for elasticache service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_elasticache.client import ElastiCacheClient

    session = get_session()
    async with session.create_client("elasticache") as client:
        client: ElastiCacheClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AuthTokenUpdateStrategyTypeType,
    AZModeType,
    ClusterModeType,
    IpDiscoveryType,
    NetworkTypeType,
    OutpostModeType,
    ServiceUpdateStatusType,
    SourceTypeType,
    TransitEncryptionModeType,
    UpdateActionStatusType,
)
from .paginator import (
    DescribeCacheClustersPaginator,
    DescribeCacheEngineVersionsPaginator,
    DescribeCacheParameterGroupsPaginator,
    DescribeCacheParametersPaginator,
    DescribeCacheSecurityGroupsPaginator,
    DescribeCacheSubnetGroupsPaginator,
    DescribeEngineDefaultParametersPaginator,
    DescribeEventsPaginator,
    DescribeGlobalReplicationGroupsPaginator,
    DescribeReplicationGroupsPaginator,
    DescribeReservedCacheNodesOfferingsPaginator,
    DescribeReservedCacheNodesPaginator,
    DescribeServerlessCacheSnapshotsPaginator,
    DescribeServerlessCachesPaginator,
    DescribeServiceUpdatesPaginator,
    DescribeSnapshotsPaginator,
    DescribeUpdateActionsPaginator,
    DescribeUserGroupsPaginator,
    DescribeUsersPaginator,
)
from .type_defs import (
    AllowedNodeTypeModificationsMessageTypeDef,
    AuthenticationModeTypeDef,
    AuthorizeCacheSecurityGroupIngressResultTypeDef,
    CacheClusterMessageTypeDef,
    CacheEngineVersionMessageTypeDef,
    CacheParameterGroupDetailsTypeDef,
    CacheParameterGroupNameMessageTypeDef,
    CacheParameterGroupsMessageTypeDef,
    CacheSecurityGroupMessageTypeDef,
    CacheSubnetGroupMessageTypeDef,
    CacheUsageLimitsTypeDef,
    CompleteMigrationResponseTypeDef,
    ConfigureShardTypeDef,
    CopyServerlessCacheSnapshotResponseTypeDef,
    CopySnapshotResultTypeDef,
    CreateCacheClusterResultTypeDef,
    CreateCacheParameterGroupResultTypeDef,
    CreateCacheSecurityGroupResultTypeDef,
    CreateCacheSubnetGroupResultTypeDef,
    CreateGlobalReplicationGroupResultTypeDef,
    CreateReplicationGroupResultTypeDef,
    CreateServerlessCacheResponseTypeDef,
    CreateServerlessCacheSnapshotResponseTypeDef,
    CreateSnapshotResultTypeDef,
    CustomerNodeEndpointTypeDef,
    DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef,
    DecreaseReplicaCountResultTypeDef,
    DeleteCacheClusterResultTypeDef,
    DeleteGlobalReplicationGroupResultTypeDef,
    DeleteReplicationGroupResultTypeDef,
    DeleteServerlessCacheResponseTypeDef,
    DeleteServerlessCacheSnapshotResponseTypeDef,
    DeleteSnapshotResultTypeDef,
    DescribeEngineDefaultParametersResultTypeDef,
    DescribeGlobalReplicationGroupsResultTypeDef,
    DescribeServerlessCacheSnapshotsResponseTypeDef,
    DescribeServerlessCachesResponseTypeDef,
    DescribeSnapshotsListMessageTypeDef,
    DescribeUserGroupsResultTypeDef,
    DescribeUsersResultTypeDef,
    DisassociateGlobalReplicationGroupResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EventsMessageTypeDef,
    ExportServerlessCacheSnapshotResponseTypeDef,
    FailoverGlobalReplicationGroupResultTypeDef,
    FilterTypeDef,
    IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef,
    IncreaseReplicaCountResultTypeDef,
    LogDeliveryConfigurationRequestTypeDef,
    ModifyCacheClusterResultTypeDef,
    ModifyCacheSubnetGroupResultTypeDef,
    ModifyGlobalReplicationGroupResultTypeDef,
    ModifyReplicationGroupResultTypeDef,
    ModifyReplicationGroupShardConfigurationResultTypeDef,
    ModifyServerlessCacheResponseTypeDef,
    NodeGroupConfigurationUnionTypeDef,
    ParameterNameValueTypeDef,
    PurchaseReservedCacheNodesOfferingResultTypeDef,
    RebalanceSlotsInGlobalReplicationGroupResultTypeDef,
    RebootCacheClusterResultTypeDef,
    RegionalConfigurationTypeDef,
    ReplicationGroupMessageTypeDef,
    ReservedCacheNodeMessageTypeDef,
    ReservedCacheNodesOfferingMessageTypeDef,
    ReshardingConfigurationTypeDef,
    RevokeCacheSecurityGroupIngressResultTypeDef,
    ServiceUpdatesMessageTypeDef,
    StartMigrationResponseTypeDef,
    TagListMessageTypeDef,
    TagTypeDef,
    TestFailoverResultTypeDef,
    TestMigrationResponseTypeDef,
    TimeRangeFilterTypeDef,
    TimestampTypeDef,
    UpdateActionResultsMessageTypeDef,
    UpdateActionsMessageTypeDef,
    UserGroupResponseTypeDef,
    UserResponseTypeDef,
)
from .waiter import (
    CacheClusterAvailableWaiter,
    CacheClusterDeletedWaiter,
    ReplicationGroupAvailableWaiter,
    ReplicationGroupDeletedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("ElastiCacheClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    APICallRateForCustomerExceededFault: Type[BotocoreClientError]
    AuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    CacheClusterAlreadyExistsFault: Type[BotocoreClientError]
    CacheClusterNotFoundFault: Type[BotocoreClientError]
    CacheParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheParameterGroupNotFoundFault: Type[BotocoreClientError]
    CacheParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSecurityGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheSecurityGroupNotFoundFault: Type[BotocoreClientError]
    CacheSecurityGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    CacheSubnetGroupInUse: Type[BotocoreClientError]
    CacheSubnetGroupNotFoundFault: Type[BotocoreClientError]
    CacheSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    CacheSubnetQuotaExceededFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterQuotaForCustomerExceededFault: Type[BotocoreClientError]
    DefaultUserAssociatedToUserGroupFault: Type[BotocoreClientError]
    DefaultUserRequired: Type[BotocoreClientError]
    DuplicateUserNameFault: Type[BotocoreClientError]
    GlobalReplicationGroupAlreadyExistsFault: Type[BotocoreClientError]
    GlobalReplicationGroupNotFoundFault: Type[BotocoreClientError]
    InsufficientCacheClusterCapacityFault: Type[BotocoreClientError]
    InvalidARNFault: Type[BotocoreClientError]
    InvalidCacheClusterStateFault: Type[BotocoreClientError]
    InvalidCacheParameterGroupStateFault: Type[BotocoreClientError]
    InvalidCacheSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidCredentialsException: Type[BotocoreClientError]
    InvalidGlobalReplicationGroupStateFault: Type[BotocoreClientError]
    InvalidKMSKeyFault: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    InvalidReplicationGroupStateFault: Type[BotocoreClientError]
    InvalidServerlessCacheSnapshotStateFault: Type[BotocoreClientError]
    InvalidServerlessCacheStateFault: Type[BotocoreClientError]
    InvalidSnapshotStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidUserGroupStateFault: Type[BotocoreClientError]
    InvalidUserStateFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    NoOperationFault: Type[BotocoreClientError]
    NodeGroupNotFoundFault: Type[BotocoreClientError]
    NodeGroupsPerReplicationGroupQuotaExceededFault: Type[BotocoreClientError]
    NodeQuotaForClusterExceededFault: Type[BotocoreClientError]
    NodeQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ReplicationGroupAlreadyExistsFault: Type[BotocoreClientError]
    ReplicationGroupAlreadyUnderMigrationFault: Type[BotocoreClientError]
    ReplicationGroupNotFoundFault: Type[BotocoreClientError]
    ReplicationGroupNotUnderMigrationFault: Type[BotocoreClientError]
    ReservedCacheNodeAlreadyExistsFault: Type[BotocoreClientError]
    ReservedCacheNodeNotFoundFault: Type[BotocoreClientError]
    ReservedCacheNodeQuotaExceededFault: Type[BotocoreClientError]
    ReservedCacheNodesOfferingNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheAlreadyExistsFault: Type[BotocoreClientError]
    ServerlessCacheNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheQuotaForCustomerExceededFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotNotFoundFault: Type[BotocoreClientError]
    ServerlessCacheSnapshotQuotaExceededFault: Type[BotocoreClientError]
    ServiceLinkedRoleNotFoundFault: Type[BotocoreClientError]
    ServiceUpdateNotFoundFault: Type[BotocoreClientError]
    SnapshotAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotFeatureNotSupportedFault: Type[BotocoreClientError]
    SnapshotNotFoundFault: Type[BotocoreClientError]
    SnapshotQuotaExceededFault: Type[BotocoreClientError]
    SubnetInUse: Type[BotocoreClientError]
    SubnetNotAllowedFault: Type[BotocoreClientError]
    TagNotFoundFault: Type[BotocoreClientError]
    TagQuotaPerResourceExceeded: Type[BotocoreClientError]
    TestFailoverNotAvailableFault: Type[BotocoreClientError]
    UserAlreadyExistsFault: Type[BotocoreClientError]
    UserGroupAlreadyExistsFault: Type[BotocoreClientError]
    UserGroupNotFoundFault: Type[BotocoreClientError]
    UserGroupQuotaExceededFault: Type[BotocoreClientError]
    UserNotFoundFault: Type[BotocoreClientError]
    UserQuotaExceededFault: Type[BotocoreClientError]

class ElastiCacheClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ElastiCacheClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#exceptions)
        """

    async def add_tags_to_resource(
        self, *, ResourceName: str, Tags: Sequence[TagTypeDef]
    ) -> TagListMessageTypeDef:
        """
        A tag is a key-value pair where the key and value are case-sensitive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.add_tags_to_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#add_tags_to_resource)
        """

    async def authorize_cache_security_group_ingress(
        self,
        *,
        CacheSecurityGroupName: str,
        EC2SecurityGroupName: str,
        EC2SecurityGroupOwnerId: str,
    ) -> AuthorizeCacheSecurityGroupIngressResultTypeDef:
        """
        Allows network ingress to a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.authorize_cache_security_group_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#authorize_cache_security_group_ingress)
        """

    async def batch_apply_update_action(
        self,
        *,
        ServiceUpdateName: str,
        ReplicationGroupIds: Sequence[str] = ...,
        CacheClusterIds: Sequence[str] = ...,
    ) -> UpdateActionResultsMessageTypeDef:
        """
        Apply the service update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.batch_apply_update_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#batch_apply_update_action)
        """

    async def batch_stop_update_action(
        self,
        *,
        ServiceUpdateName: str,
        ReplicationGroupIds: Sequence[str] = ...,
        CacheClusterIds: Sequence[str] = ...,
    ) -> UpdateActionResultsMessageTypeDef:
        """
        Stop the service update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.batch_stop_update_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#batch_stop_update_action)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#close)
        """

    async def complete_migration(
        self, *, ReplicationGroupId: str, Force: bool = ...
    ) -> CompleteMigrationResponseTypeDef:
        """
        Complete the migration of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.complete_migration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#complete_migration)
        """

    async def copy_serverless_cache_snapshot(
        self,
        *,
        SourceServerlessCacheSnapshotName: str,
        TargetServerlessCacheSnapshotName: str,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CopyServerlessCacheSnapshotResponseTypeDef:
        """
        Creates a copy of an existing serverless cache's snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.copy_serverless_cache_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#copy_serverless_cache_snapshot)
        """

    async def copy_snapshot(
        self,
        *,
        SourceSnapshotName: str,
        TargetSnapshotName: str,
        TargetBucket: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CopySnapshotResultTypeDef:
        """
        Makes a copy of an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.copy_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#copy_snapshot)
        """

    async def create_cache_cluster(
        self,
        *,
        CacheClusterId: str,
        ReplicationGroupId: str = ...,
        AZMode: AZModeType = ...,
        PreferredAvailabilityZone: str = ...,
        PreferredAvailabilityZones: Sequence[str] = ...,
        NumCacheNodes: int = ...,
        CacheNodeType: str = ...,
        Engine: str = ...,
        EngineVersion: str = ...,
        CacheParameterGroupName: str = ...,
        CacheSubnetGroupName: str = ...,
        CacheSecurityGroupNames: Sequence[str] = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SnapshotArns: Sequence[str] = ...,
        SnapshotName: str = ...,
        PreferredMaintenanceWindow: str = ...,
        Port: int = ...,
        NotificationTopicArn: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        SnapshotRetentionLimit: int = ...,
        SnapshotWindow: str = ...,
        AuthToken: str = ...,
        OutpostMode: OutpostModeType = ...,
        PreferredOutpostArn: str = ...,
        PreferredOutpostArns: Sequence[str] = ...,
        LogDeliveryConfigurations: Sequence[LogDeliveryConfigurationRequestTypeDef] = ...,
        TransitEncryptionEnabled: bool = ...,
        NetworkType: NetworkTypeType = ...,
        IpDiscovery: IpDiscoveryType = ...,
    ) -> CreateCacheClusterResultTypeDef:
        """
        Creates a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_cache_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_cache_cluster)
        """

    async def create_cache_parameter_group(
        self,
        *,
        CacheParameterGroupName: str,
        CacheParameterGroupFamily: str,
        Description: str,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateCacheParameterGroupResultTypeDef:
        """
        Creates a new Amazon ElastiCache cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_cache_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_cache_parameter_group)
        """

    async def create_cache_security_group(
        self, *, CacheSecurityGroupName: str, Description: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateCacheSecurityGroupResultTypeDef:
        """
        Creates a new cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_cache_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_cache_security_group)
        """

    async def create_cache_subnet_group(
        self,
        *,
        CacheSubnetGroupName: str,
        CacheSubnetGroupDescription: str,
        SubnetIds: Sequence[str],
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateCacheSubnetGroupResultTypeDef:
        """
        Creates a new cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_cache_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_cache_subnet_group)
        """

    async def create_global_replication_group(
        self,
        *,
        GlobalReplicationGroupIdSuffix: str,
        PrimaryReplicationGroupId: str,
        GlobalReplicationGroupDescription: str = ...,
    ) -> CreateGlobalReplicationGroupResultTypeDef:
        """
        Global Datastore for Redis OSS offers fully managed, fast, reliable and secure
        cross-region
        replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_global_replication_group)
        """

    async def create_replication_group(
        self,
        *,
        ReplicationGroupId: str,
        ReplicationGroupDescription: str,
        GlobalReplicationGroupId: str = ...,
        PrimaryClusterId: str = ...,
        AutomaticFailoverEnabled: bool = ...,
        MultiAZEnabled: bool = ...,
        NumCacheClusters: int = ...,
        PreferredCacheClusterAZs: Sequence[str] = ...,
        NumNodeGroups: int = ...,
        ReplicasPerNodeGroup: int = ...,
        NodeGroupConfiguration: Sequence[NodeGroupConfigurationUnionTypeDef] = ...,
        CacheNodeType: str = ...,
        Engine: str = ...,
        EngineVersion: str = ...,
        CacheParameterGroupName: str = ...,
        CacheSubnetGroupName: str = ...,
        CacheSecurityGroupNames: Sequence[str] = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SnapshotArns: Sequence[str] = ...,
        SnapshotName: str = ...,
        PreferredMaintenanceWindow: str = ...,
        Port: int = ...,
        NotificationTopicArn: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        SnapshotRetentionLimit: int = ...,
        SnapshotWindow: str = ...,
        AuthToken: str = ...,
        TransitEncryptionEnabled: bool = ...,
        AtRestEncryptionEnabled: bool = ...,
        KmsKeyId: str = ...,
        UserGroupIds: Sequence[str] = ...,
        LogDeliveryConfigurations: Sequence[LogDeliveryConfigurationRequestTypeDef] = ...,
        DataTieringEnabled: bool = ...,
        NetworkType: NetworkTypeType = ...,
        IpDiscovery: IpDiscoveryType = ...,
        TransitEncryptionMode: TransitEncryptionModeType = ...,
        ClusterMode: ClusterModeType = ...,
        ServerlessCacheSnapshotName: str = ...,
    ) -> CreateReplicationGroupResultTypeDef:
        """
        Creates a Redis OSS (cluster mode disabled) or a Redis OSS (cluster mode
        enabled) replication
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_replication_group)
        """

    async def create_serverless_cache(
        self,
        *,
        ServerlessCacheName: str,
        Engine: str,
        Description: str = ...,
        MajorEngineVersion: str = ...,
        CacheUsageLimits: CacheUsageLimitsTypeDef = ...,
        KmsKeyId: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        SnapshotArnsToRestore: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        UserGroupId: str = ...,
        SubnetIds: Sequence[str] = ...,
        SnapshotRetentionLimit: int = ...,
        DailySnapshotTime: str = ...,
    ) -> CreateServerlessCacheResponseTypeDef:
        """
        Creates a serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_serverless_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_serverless_cache)
        """

    async def create_serverless_cache_snapshot(
        self,
        *,
        ServerlessCacheSnapshotName: str,
        ServerlessCacheName: str,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateServerlessCacheSnapshotResponseTypeDef:
        """
        This API creates a copy of an entire ServerlessCache at a specific moment in
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_serverless_cache_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_serverless_cache_snapshot)
        """

    async def create_snapshot(
        self,
        *,
        SnapshotName: str,
        ReplicationGroupId: str = ...,
        CacheClusterId: str = ...,
        KmsKeyId: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateSnapshotResultTypeDef:
        """
        Creates a copy of an entire cluster or replication group at a specific moment
        in
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_snapshot)
        """

    async def create_user(
        self,
        *,
        UserId: str,
        UserName: str,
        Engine: str,
        AccessString: str,
        Passwords: Sequence[str] = ...,
        NoPasswordRequired: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
        AuthenticationMode: AuthenticationModeTypeDef = ...,
    ) -> UserResponseTypeDef:
        """
        For Redis OSS engine version 6.0 onwards: Creates a Redis OSS user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_user)
        """

    async def create_user_group(
        self,
        *,
        UserGroupId: str,
        Engine: str,
        UserIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> UserGroupResponseTypeDef:
        """
        For Redis OSS engine version 6.0 onwards: Creates a Redis OSS user group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.create_user_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#create_user_group)
        """

    async def decrease_node_groups_in_global_replication_group(
        self,
        *,
        GlobalReplicationGroupId: str,
        NodeGroupCount: int,
        ApplyImmediately: bool,
        GlobalNodeGroupsToRemove: Sequence[str] = ...,
        GlobalNodeGroupsToRetain: Sequence[str] = ...,
    ) -> DecreaseNodeGroupsInGlobalReplicationGroupResultTypeDef:
        """
        Decreases the number of node groups in a Global datastore See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/elasticache-2015-02-02/DecreaseNodeGroupsInGlobalReplicationGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.decrease_node_groups_in_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#decrease_node_groups_in_global_replication_group)
        """

    async def decrease_replica_count(
        self,
        *,
        ReplicationGroupId: str,
        ApplyImmediately: bool,
        NewReplicaCount: int = ...,
        ReplicaConfiguration: Sequence[ConfigureShardTypeDef] = ...,
        ReplicasToRemove: Sequence[str] = ...,
    ) -> DecreaseReplicaCountResultTypeDef:
        """
        Dynamically decreases the number of replicas in a Redis OSS (cluster mode
        disabled) replication group or the number of replica nodes in one or more node
        groups (shards) of a Redis OSS (cluster mode enabled) replication
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.decrease_replica_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#decrease_replica_count)
        """

    async def delete_cache_cluster(
        self, *, CacheClusterId: str, FinalSnapshotIdentifier: str = ...
    ) -> DeleteCacheClusterResultTypeDef:
        """
        Deletes a previously provisioned cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_cache_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_cache_cluster)
        """

    async def delete_cache_parameter_group(
        self, *, CacheParameterGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_cache_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_cache_parameter_group)
        """

    async def delete_cache_security_group(
        self, *, CacheSecurityGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_cache_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_cache_security_group)
        """

    async def delete_cache_subnet_group(
        self, *, CacheSubnetGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_cache_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_cache_subnet_group)
        """

    async def delete_global_replication_group(
        self, *, GlobalReplicationGroupId: str, RetainPrimaryReplicationGroup: bool
    ) -> DeleteGlobalReplicationGroupResultTypeDef:
        """
        Deleting a Global datastore is a two-step process: * First, you must
        DisassociateGlobalReplicationGroup to remove the secondary clusters in the
        Global
        datastore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_global_replication_group)
        """

    async def delete_replication_group(
        self,
        *,
        ReplicationGroupId: str,
        RetainPrimaryCluster: bool = ...,
        FinalSnapshotIdentifier: str = ...,
    ) -> DeleteReplicationGroupResultTypeDef:
        """
        Deletes an existing replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_replication_group)
        """

    async def delete_serverless_cache(
        self, *, ServerlessCacheName: str, FinalSnapshotName: str = ...
    ) -> DeleteServerlessCacheResponseTypeDef:
        """
        Deletes a specified existing serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_serverless_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_serverless_cache)
        """

    async def delete_serverless_cache_snapshot(
        self, *, ServerlessCacheSnapshotName: str
    ) -> DeleteServerlessCacheSnapshotResponseTypeDef:
        """
        Deletes an existing serverless cache snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_serverless_cache_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_serverless_cache_snapshot)
        """

    async def delete_snapshot(self, *, SnapshotName: str) -> DeleteSnapshotResultTypeDef:
        """
        Deletes an existing snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_snapshot)
        """

    async def delete_user(self, *, UserId: str) -> UserResponseTypeDef:
        """
        For Redis OSS engine version 6.0 onwards: Deletes a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_user)
        """

    async def delete_user_group(self, *, UserGroupId: str) -> UserGroupResponseTypeDef:
        """
        For Redis OSS engine version 6.0 onwards: Deletes a user group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.delete_user_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#delete_user_group)
        """

    async def describe_cache_clusters(
        self,
        *,
        CacheClusterId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        ShowCacheNodeInfo: bool = ...,
        ShowCacheClustersNotInReplicationGroups: bool = ...,
    ) -> CacheClusterMessageTypeDef:
        """
        Returns information about all provisioned clusters if no cluster identifier is
        specified, or about a specific cache cluster if a cluster identifier is
        supplied.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_clusters)
        """

    async def describe_cache_engine_versions(
        self,
        *,
        Engine: str = ...,
        EngineVersion: str = ...,
        CacheParameterGroupFamily: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        DefaultOnly: bool = ...,
    ) -> CacheEngineVersionMessageTypeDef:
        """
        Returns a list of the available cache engines and their versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_engine_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_engine_versions)
        """

    async def describe_cache_parameter_groups(
        self, *, CacheParameterGroupName: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> CacheParameterGroupsMessageTypeDef:
        """
        Returns a list of cache parameter group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_parameter_groups)
        """

    async def describe_cache_parameters(
        self,
        *,
        CacheParameterGroupName: str,
        Source: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> CacheParameterGroupDetailsTypeDef:
        """
        Returns the detailed parameter list for a particular cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_parameters)
        """

    async def describe_cache_security_groups(
        self, *, CacheSecurityGroupName: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> CacheSecurityGroupMessageTypeDef:
        """
        Returns a list of cache security group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_security_groups)
        """

    async def describe_cache_subnet_groups(
        self, *, CacheSubnetGroupName: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> CacheSubnetGroupMessageTypeDef:
        """
        Returns a list of cache subnet group descriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_cache_subnet_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_cache_subnet_groups)
        """

    async def describe_engine_default_parameters(
        self, *, CacheParameterGroupFamily: str, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeEngineDefaultParametersResultTypeDef:
        """
        Returns the default engine and system parameter information for the specified
        cache
        engine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_engine_default_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_engine_default_parameters)
        """

    async def describe_events(
        self,
        *,
        SourceIdentifier: str = ...,
        SourceType: SourceTypeType = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        Duration: int = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> EventsMessageTypeDef:
        """
        Returns events related to clusters, cache security groups, and cache parameter
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_events)
        """

    async def describe_global_replication_groups(
        self,
        *,
        GlobalReplicationGroupId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        ShowMemberInfo: bool = ...,
    ) -> DescribeGlobalReplicationGroupsResultTypeDef:
        """
        Returns information about a particular global replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_global_replication_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_global_replication_groups)
        """

    async def describe_replication_groups(
        self, *, ReplicationGroupId: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> ReplicationGroupMessageTypeDef:
        """
        Returns information about a particular replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_replication_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_replication_groups)
        """

    async def describe_reserved_cache_nodes(
        self,
        *,
        ReservedCacheNodeId: str = ...,
        ReservedCacheNodesOfferingId: str = ...,
        CacheNodeType: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ReservedCacheNodeMessageTypeDef:
        """
        Returns information about reserved cache nodes for this account, or about a
        specified reserved cache
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_reserved_cache_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_reserved_cache_nodes)
        """

    async def describe_reserved_cache_nodes_offerings(
        self,
        *,
        ReservedCacheNodesOfferingId: str = ...,
        CacheNodeType: str = ...,
        Duration: str = ...,
        ProductDescription: str = ...,
        OfferingType: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ReservedCacheNodesOfferingMessageTypeDef:
        """
        Lists available reserved cache node offerings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_reserved_cache_nodes_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_reserved_cache_nodes_offerings)
        """

    async def describe_serverless_cache_snapshots(
        self,
        *,
        ServerlessCacheName: str = ...,
        ServerlessCacheSnapshotName: str = ...,
        SnapshotType: str = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> DescribeServerlessCacheSnapshotsResponseTypeDef:
        """
        Returns information about serverless cache snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_serverless_cache_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_serverless_cache_snapshots)
        """

    async def describe_serverless_caches(
        self, *, ServerlessCacheName: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeServerlessCachesResponseTypeDef:
        """
        Returns information about a specific serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_serverless_caches)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_serverless_caches)
        """

    async def describe_service_updates(
        self,
        *,
        ServiceUpdateName: str = ...,
        ServiceUpdateStatus: Sequence[ServiceUpdateStatusType] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ServiceUpdatesMessageTypeDef:
        """
        Returns details of the service updates See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/elasticache-2015-02-02/DescribeServiceUpdates).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_service_updates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_service_updates)
        """

    async def describe_snapshots(
        self,
        *,
        ReplicationGroupId: str = ...,
        CacheClusterId: str = ...,
        SnapshotName: str = ...,
        SnapshotSource: str = ...,
        Marker: str = ...,
        MaxRecords: int = ...,
        ShowNodeGroupConfig: bool = ...,
    ) -> DescribeSnapshotsListMessageTypeDef:
        """
        Returns information about cluster or replication group snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_snapshots)
        """

    async def describe_update_actions(
        self,
        *,
        ServiceUpdateName: str = ...,
        ReplicationGroupIds: Sequence[str] = ...,
        CacheClusterIds: Sequence[str] = ...,
        Engine: str = ...,
        ServiceUpdateStatus: Sequence[ServiceUpdateStatusType] = ...,
        ServiceUpdateTimeRange: TimeRangeFilterTypeDef = ...,
        UpdateActionStatus: Sequence[UpdateActionStatusType] = ...,
        ShowNodeLevelUpdateStatus: bool = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> UpdateActionsMessageTypeDef:
        """
        Returns details of the update actions See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/elasticache-2015-02-02/DescribeUpdateActions).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_update_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_update_actions)
        """

    async def describe_user_groups(
        self, *, UserGroupId: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeUserGroupsResultTypeDef:
        """
        Returns a list of user groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_user_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_user_groups)
        """

    async def describe_users(
        self,
        *,
        Engine: str = ...,
        UserId: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> DescribeUsersResultTypeDef:
        """
        Returns a list of users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.describe_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#describe_users)
        """

    async def disassociate_global_replication_group(
        self, *, GlobalReplicationGroupId: str, ReplicationGroupId: str, ReplicationGroupRegion: str
    ) -> DisassociateGlobalReplicationGroupResultTypeDef:
        """
        Remove a secondary cluster from the Global datastore using the Global datastore
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.disassociate_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#disassociate_global_replication_group)
        """

    async def export_serverless_cache_snapshot(
        self, *, ServerlessCacheSnapshotName: str, S3BucketName: str
    ) -> ExportServerlessCacheSnapshotResponseTypeDef:
        """
        Provides the functionality to export the serverless cache snapshot data to
        Amazon
        S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.export_serverless_cache_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#export_serverless_cache_snapshot)
        """

    async def failover_global_replication_group(
        self, *, GlobalReplicationGroupId: str, PrimaryRegion: str, PrimaryReplicationGroupId: str
    ) -> FailoverGlobalReplicationGroupResultTypeDef:
        """
        Used to failover the primary region to a secondary region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.failover_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#failover_global_replication_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#generate_presigned_url)
        """

    async def increase_node_groups_in_global_replication_group(
        self,
        *,
        GlobalReplicationGroupId: str,
        NodeGroupCount: int,
        ApplyImmediately: bool,
        RegionalConfigurations: Sequence[RegionalConfigurationTypeDef] = ...,
    ) -> IncreaseNodeGroupsInGlobalReplicationGroupResultTypeDef:
        """
        Increase the number of node groups in the Global datastore See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/elasticache-2015-02-02/IncreaseNodeGroupsInGlobalReplicationGroup).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.increase_node_groups_in_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#increase_node_groups_in_global_replication_group)
        """

    async def increase_replica_count(
        self,
        *,
        ReplicationGroupId: str,
        ApplyImmediately: bool,
        NewReplicaCount: int = ...,
        ReplicaConfiguration: Sequence[ConfigureShardTypeDef] = ...,
    ) -> IncreaseReplicaCountResultTypeDef:
        """
        Dynamically increases the number of replicas in a Redis OSS (cluster mode
        disabled) replication group or the number of replica nodes in one or more node
        groups (shards) of a Redis OSS (cluster mode enabled) replication
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.increase_replica_count)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#increase_replica_count)
        """

    async def list_allowed_node_type_modifications(
        self, *, CacheClusterId: str = ..., ReplicationGroupId: str = ...
    ) -> AllowedNodeTypeModificationsMessageTypeDef:
        """
        Lists all available node types that you can scale your Redis OSS cluster's or
        replication group's current node
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.list_allowed_node_type_modifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#list_allowed_node_type_modifications)
        """

    async def list_tags_for_resource(self, *, ResourceName: str) -> TagListMessageTypeDef:
        """
        Lists all tags currently on a named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#list_tags_for_resource)
        """

    async def modify_cache_cluster(
        self,
        *,
        CacheClusterId: str,
        NumCacheNodes: int = ...,
        CacheNodeIdsToRemove: Sequence[str] = ...,
        AZMode: AZModeType = ...,
        NewAvailabilityZones: Sequence[str] = ...,
        CacheSecurityGroupNames: Sequence[str] = ...,
        SecurityGroupIds: Sequence[str] = ...,
        PreferredMaintenanceWindow: str = ...,
        NotificationTopicArn: str = ...,
        CacheParameterGroupName: str = ...,
        NotificationTopicStatus: str = ...,
        ApplyImmediately: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        SnapshotRetentionLimit: int = ...,
        SnapshotWindow: str = ...,
        CacheNodeType: str = ...,
        AuthToken: str = ...,
        AuthTokenUpdateStrategy: AuthTokenUpdateStrategyTypeType = ...,
        LogDeliveryConfigurations: Sequence[LogDeliveryConfigurationRequestTypeDef] = ...,
        IpDiscovery: IpDiscoveryType = ...,
    ) -> ModifyCacheClusterResultTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_cache_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_cache_cluster)
        """

    async def modify_cache_parameter_group(
        self,
        *,
        CacheParameterGroupName: str,
        ParameterNameValues: Sequence[ParameterNameValueTypeDef],
    ) -> CacheParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cache parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_cache_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_cache_parameter_group)
        """

    async def modify_cache_subnet_group(
        self,
        *,
        CacheSubnetGroupName: str,
        CacheSubnetGroupDescription: str = ...,
        SubnetIds: Sequence[str] = ...,
    ) -> ModifyCacheSubnetGroupResultTypeDef:
        """
        Modifies an existing cache subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_cache_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_cache_subnet_group)
        """

    async def modify_global_replication_group(
        self,
        *,
        GlobalReplicationGroupId: str,
        ApplyImmediately: bool,
        CacheNodeType: str = ...,
        EngineVersion: str = ...,
        CacheParameterGroupName: str = ...,
        GlobalReplicationGroupDescription: str = ...,
        AutomaticFailoverEnabled: bool = ...,
    ) -> ModifyGlobalReplicationGroupResultTypeDef:
        """
        Modifies the settings for a Global datastore.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_global_replication_group)
        """

    async def modify_replication_group(
        self,
        *,
        ReplicationGroupId: str,
        ReplicationGroupDescription: str = ...,
        PrimaryClusterId: str = ...,
        SnapshottingClusterId: str = ...,
        AutomaticFailoverEnabled: bool = ...,
        MultiAZEnabled: bool = ...,
        NodeGroupId: str = ...,
        CacheSecurityGroupNames: Sequence[str] = ...,
        SecurityGroupIds: Sequence[str] = ...,
        PreferredMaintenanceWindow: str = ...,
        NotificationTopicArn: str = ...,
        CacheParameterGroupName: str = ...,
        NotificationTopicStatus: str = ...,
        ApplyImmediately: bool = ...,
        EngineVersion: str = ...,
        AutoMinorVersionUpgrade: bool = ...,
        SnapshotRetentionLimit: int = ...,
        SnapshotWindow: str = ...,
        CacheNodeType: str = ...,
        AuthToken: str = ...,
        AuthTokenUpdateStrategy: AuthTokenUpdateStrategyTypeType = ...,
        UserGroupIdsToAdd: Sequence[str] = ...,
        UserGroupIdsToRemove: Sequence[str] = ...,
        RemoveUserGroups: bool = ...,
        LogDeliveryConfigurations: Sequence[LogDeliveryConfigurationRequestTypeDef] = ...,
        IpDiscovery: IpDiscoveryType = ...,
        TransitEncryptionEnabled: bool = ...,
        TransitEncryptionMode: TransitEncryptionModeType = ...,
        ClusterMode: ClusterModeType = ...,
    ) -> ModifyReplicationGroupResultTypeDef:
        """
        Modifies the settings for a replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_replication_group)
        """

    async def modify_replication_group_shard_configuration(
        self,
        *,
        ReplicationGroupId: str,
        NodeGroupCount: int,
        ApplyImmediately: bool,
        ReshardingConfiguration: Sequence[ReshardingConfigurationTypeDef] = ...,
        NodeGroupsToRemove: Sequence[str] = ...,
        NodeGroupsToRetain: Sequence[str] = ...,
    ) -> ModifyReplicationGroupShardConfigurationResultTypeDef:
        """
        Modifies a replication group's shards (node groups) by allowing you to add
        shards, remove shards, or rebalance the keyspaces among existing
        shards.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_replication_group_shard_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_replication_group_shard_configuration)
        """

    async def modify_serverless_cache(
        self,
        *,
        ServerlessCacheName: str,
        Description: str = ...,
        CacheUsageLimits: CacheUsageLimitsTypeDef = ...,
        RemoveUserGroup: bool = ...,
        UserGroupId: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        SnapshotRetentionLimit: int = ...,
        DailySnapshotTime: str = ...,
    ) -> ModifyServerlessCacheResponseTypeDef:
        """
        This API modifies the attributes of a serverless cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_serverless_cache)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_serverless_cache)
        """

    async def modify_user(
        self,
        *,
        UserId: str,
        AccessString: str = ...,
        AppendAccessString: str = ...,
        Passwords: Sequence[str] = ...,
        NoPasswordRequired: bool = ...,
        AuthenticationMode: AuthenticationModeTypeDef = ...,
    ) -> UserResponseTypeDef:
        """
        Changes user password(s) and/or access string.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_user)
        """

    async def modify_user_group(
        self,
        *,
        UserGroupId: str,
        UserIdsToAdd: Sequence[str] = ...,
        UserIdsToRemove: Sequence[str] = ...,
    ) -> UserGroupResponseTypeDef:
        """
        Changes the list of users that belong to the user group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.modify_user_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#modify_user_group)
        """

    async def purchase_reserved_cache_nodes_offering(
        self,
        *,
        ReservedCacheNodesOfferingId: str,
        ReservedCacheNodeId: str = ...,
        CacheNodeCount: int = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> PurchaseReservedCacheNodesOfferingResultTypeDef:
        """
        Allows you to purchase a reserved cache node offering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.purchase_reserved_cache_nodes_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#purchase_reserved_cache_nodes_offering)
        """

    async def rebalance_slots_in_global_replication_group(
        self, *, GlobalReplicationGroupId: str, ApplyImmediately: bool
    ) -> RebalanceSlotsInGlobalReplicationGroupResultTypeDef:
        """
        Redistribute slots to ensure uniform distribution across existing shards in the
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.rebalance_slots_in_global_replication_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#rebalance_slots_in_global_replication_group)
        """

    async def reboot_cache_cluster(
        self, *, CacheClusterId: str, CacheNodeIdsToReboot: Sequence[str]
    ) -> RebootCacheClusterResultTypeDef:
        """
        Reboots some, or all, of the cache nodes within a provisioned cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.reboot_cache_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#reboot_cache_cluster)
        """

    async def remove_tags_from_resource(
        self, *, ResourceName: str, TagKeys: Sequence[str]
    ) -> TagListMessageTypeDef:
        """
        Removes the tags identified by the `TagKeys` list from the named resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.remove_tags_from_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#remove_tags_from_resource)
        """

    async def reset_cache_parameter_group(
        self,
        *,
        CacheParameterGroupName: str,
        ResetAllParameters: bool = ...,
        ParameterNameValues: Sequence[ParameterNameValueTypeDef] = ...,
    ) -> CacheParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a cache parameter group to the engine or system
        default
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.reset_cache_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#reset_cache_parameter_group)
        """

    async def revoke_cache_security_group_ingress(
        self,
        *,
        CacheSecurityGroupName: str,
        EC2SecurityGroupName: str,
        EC2SecurityGroupOwnerId: str,
    ) -> RevokeCacheSecurityGroupIngressResultTypeDef:
        """
        Revokes ingress from a cache security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.revoke_cache_security_group_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#revoke_cache_security_group_ingress)
        """

    async def start_migration(
        self,
        *,
        ReplicationGroupId: str,
        CustomerNodeEndpointList: Sequence[CustomerNodeEndpointTypeDef],
    ) -> StartMigrationResponseTypeDef:
        """
        Start the migration of data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.start_migration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#start_migration)
        """

    async def test_failover(
        self, *, ReplicationGroupId: str, NodeGroupId: str
    ) -> TestFailoverResultTypeDef:
        """
        Represents the input of a `TestFailover` operation which tests automatic
        failover on a specified node group (called shard in the console) in a
        replication group (called cluster in the
        console).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.test_failover)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#test_failover)
        """

    async def test_migration(
        self,
        *,
        ReplicationGroupId: str,
        CustomerNodeEndpointList: Sequence[CustomerNodeEndpointTypeDef],
    ) -> TestMigrationResponseTypeDef:
        """
        Async API to test connection between source and target replication group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.test_migration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#test_migration)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_clusters"]
    ) -> DescribeCacheClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_engine_versions"]
    ) -> DescribeCacheEngineVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_parameter_groups"]
    ) -> DescribeCacheParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_parameters"]
    ) -> DescribeCacheParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_security_groups"]
    ) -> DescribeCacheSecurityGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cache_subnet_groups"]
    ) -> DescribeCacheSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_engine_default_parameters"]
    ) -> DescribeEngineDefaultParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_global_replication_groups"]
    ) -> DescribeGlobalReplicationGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_groups"]
    ) -> DescribeReplicationGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_cache_nodes"]
    ) -> DescribeReservedCacheNodesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_cache_nodes_offerings"]
    ) -> DescribeReservedCacheNodesOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_serverless_cache_snapshots"]
    ) -> DescribeServerlessCacheSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_serverless_caches"]
    ) -> DescribeServerlessCachesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_service_updates"]
    ) -> DescribeServiceUpdatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshots"]
    ) -> DescribeSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_update_actions"]
    ) -> DescribeUpdateActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_user_groups"]
    ) -> DescribeUserGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_paginator)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["cache_cluster_available"]
    ) -> CacheClusterAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["cache_cluster_deleted"]
    ) -> CacheClusterDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_group_available"]
    ) -> ReplicationGroupAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_waiter)
        """

    @overload
    def get_waiter(
        self, waiter_name: Literal["replication_group_deleted"]
    ) -> ReplicationGroupDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/#get_waiter)
        """

    async def __aenter__(self) -> "ElastiCacheClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elasticache/client/)
        """
