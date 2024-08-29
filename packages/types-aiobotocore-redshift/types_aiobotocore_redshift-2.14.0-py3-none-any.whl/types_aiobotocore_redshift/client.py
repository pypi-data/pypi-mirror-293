"""
Type annotations for redshift service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_redshift.client import RedshiftClient

    session = get_session()
    async with session.create_client("redshift") as client:
        client: RedshiftClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionTypeType,
    AquaConfigurationStatusType,
    DataShareStatusForConsumerType,
    DataShareStatusForProducerType,
    LogDestinationTypeType,
    PartnerIntegrationStatusType,
    ReservedNodeExchangeActionTypeType,
    ScheduledActionTypeValuesType,
    SourceTypeType,
    UsageLimitBreachActionType,
    UsageLimitFeatureTypeType,
    UsageLimitLimitTypeType,
    UsageLimitPeriodType,
)
from .paginator import (
    DescribeClusterDbRevisionsPaginator,
    DescribeClusterParameterGroupsPaginator,
    DescribeClusterParametersPaginator,
    DescribeClusterSecurityGroupsPaginator,
    DescribeClusterSnapshotsPaginator,
    DescribeClustersPaginator,
    DescribeClusterSubnetGroupsPaginator,
    DescribeClusterTracksPaginator,
    DescribeClusterVersionsPaginator,
    DescribeCustomDomainAssociationsPaginator,
    DescribeDataSharesForConsumerPaginator,
    DescribeDataSharesForProducerPaginator,
    DescribeDataSharesPaginator,
    DescribeDefaultClusterParametersPaginator,
    DescribeEndpointAccessPaginator,
    DescribeEndpointAuthorizationPaginator,
    DescribeEventsPaginator,
    DescribeEventSubscriptionsPaginator,
    DescribeHsmClientCertificatesPaginator,
    DescribeHsmConfigurationsPaginator,
    DescribeInboundIntegrationsPaginator,
    DescribeNodeConfigurationOptionsPaginator,
    DescribeOrderableClusterOptionsPaginator,
    DescribeRedshiftIdcApplicationsPaginator,
    DescribeReservedNodeExchangeStatusPaginator,
    DescribeReservedNodeOfferingsPaginator,
    DescribeReservedNodesPaginator,
    DescribeScheduledActionsPaginator,
    DescribeSnapshotCopyGrantsPaginator,
    DescribeSnapshotSchedulesPaginator,
    DescribeTableRestoreStatusPaginator,
    DescribeTagsPaginator,
    DescribeUsageLimitsPaginator,
    GetReservedNodeExchangeConfigurationOptionsPaginator,
    GetReservedNodeExchangeOfferingsPaginator,
    ListRecommendationsPaginator,
)
from .type_defs import (
    AcceptReservedNodeExchangeOutputMessageTypeDef,
    AccountAttributeListTypeDef,
    AuthorizeClusterSecurityGroupIngressResultTypeDef,
    AuthorizedTokenIssuerUnionTypeDef,
    AuthorizeSnapshotAccessResultTypeDef,
    BatchDeleteClusterSnapshotsResultTypeDef,
    BatchModifyClusterSnapshotsOutputMessageTypeDef,
    ClusterCredentialsTypeDef,
    ClusterDbRevisionsMessageTypeDef,
    ClusterExtendedCredentialsTypeDef,
    ClusterParameterGroupDetailsTypeDef,
    ClusterParameterGroupNameMessageTypeDef,
    ClusterParameterGroupsMessageTypeDef,
    ClusterSecurityGroupMessageTypeDef,
    ClustersMessageTypeDef,
    ClusterSubnetGroupMessageTypeDef,
    ClusterVersionsMessageTypeDef,
    CopyClusterSnapshotResultTypeDef,
    CreateAuthenticationProfileResultTypeDef,
    CreateClusterParameterGroupResultTypeDef,
    CreateClusterResultTypeDef,
    CreateClusterSecurityGroupResultTypeDef,
    CreateClusterSnapshotResultTypeDef,
    CreateClusterSubnetGroupResultTypeDef,
    CreateCustomDomainAssociationResultTypeDef,
    CreateEventSubscriptionResultTypeDef,
    CreateHsmClientCertificateResultTypeDef,
    CreateHsmConfigurationResultTypeDef,
    CreateRedshiftIdcApplicationResultTypeDef,
    CreateSnapshotCopyGrantResultTypeDef,
    CustomDomainAssociationsMessageTypeDef,
    CustomerStorageMessageTypeDef,
    DataShareResponseTypeDef,
    DeleteAuthenticationProfileResultTypeDef,
    DeleteClusterResultTypeDef,
    DeleteClusterSnapshotMessageTypeDef,
    DeleteClusterSnapshotResultTypeDef,
    DescribeAuthenticationProfilesResultTypeDef,
    DescribeDataSharesForConsumerResultTypeDef,
    DescribeDataSharesForProducerResultTypeDef,
    DescribeDataSharesResultTypeDef,
    DescribeDefaultClusterParametersResultTypeDef,
    DescribePartnersOutputMessageTypeDef,
    DescribeRedshiftIdcApplicationsResultTypeDef,
    DescribeReservedNodeExchangeStatusOutputMessageTypeDef,
    DescribeSnapshotSchedulesOutputMessageTypeDef,
    DisableSnapshotCopyResultTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableSnapshotCopyResultTypeDef,
    EndpointAccessListTypeDef,
    EndpointAccessResponseTypeDef,
    EndpointAuthorizationListTypeDef,
    EndpointAuthorizationResponseTypeDef,
    EventCategoriesMessageTypeDef,
    EventsMessageTypeDef,
    EventSubscriptionsMessageTypeDef,
    FailoverPrimaryComputeResultTypeDef,
    GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef,
    GetReservedNodeExchangeOfferingsOutputMessageTypeDef,
    GetResourcePolicyResultTypeDef,
    HsmClientCertificateMessageTypeDef,
    HsmConfigurationMessageTypeDef,
    InboundIntegrationsMessageTypeDef,
    ListRecommendationsResultTypeDef,
    LoggingStatusTypeDef,
    ModifyAquaOutputMessageTypeDef,
    ModifyAuthenticationProfileResultTypeDef,
    ModifyClusterDbRevisionResultTypeDef,
    ModifyClusterIamRolesResultTypeDef,
    ModifyClusterMaintenanceResultTypeDef,
    ModifyClusterResultTypeDef,
    ModifyClusterSnapshotResultTypeDef,
    ModifyClusterSubnetGroupResultTypeDef,
    ModifyCustomDomainAssociationResultTypeDef,
    ModifyEventSubscriptionResultTypeDef,
    ModifyRedshiftIdcApplicationResultTypeDef,
    ModifySnapshotCopyRetentionPeriodResultTypeDef,
    NodeConfigurationOptionsFilterTypeDef,
    NodeConfigurationOptionsMessageTypeDef,
    OrderableClusterOptionsMessageTypeDef,
    ParameterTypeDef,
    PartnerIntegrationOutputMessageTypeDef,
    PauseClusterResultTypeDef,
    PurchaseReservedNodeOfferingResultTypeDef,
    PutResourcePolicyResultTypeDef,
    RebootClusterResultTypeDef,
    ReservedNodeOfferingsMessageTypeDef,
    ReservedNodesMessageTypeDef,
    ResizeClusterResultTypeDef,
    ResizeProgressMessageTypeDef,
    RestoreFromClusterSnapshotResultTypeDef,
    RestoreTableFromClusterSnapshotResultTypeDef,
    ResumeClusterResultTypeDef,
    RevokeClusterSecurityGroupIngressResultTypeDef,
    RevokeSnapshotAccessResultTypeDef,
    RotateEncryptionKeyResultTypeDef,
    ScheduledActionFilterTypeDef,
    ScheduledActionResponseTypeDef,
    ScheduledActionsMessageTypeDef,
    ScheduledActionTypeTypeDef,
    ServiceIntegrationsUnionUnionTypeDef,
    SnapshotCopyGrantMessageTypeDef,
    SnapshotMessageTypeDef,
    SnapshotScheduleResponseTypeDef,
    SnapshotSortingEntityTypeDef,
    TableRestoreStatusMessageTypeDef,
    TaggedResourceListMessageTypeDef,
    TagTypeDef,
    TimestampTypeDef,
    TrackListMessageTypeDef,
    UsageLimitListTypeDef,
    UsageLimitResponseTypeDef,
)
from .waiter import (
    ClusterAvailableWaiter,
    ClusterDeletedWaiter,
    ClusterRestoredWaiter,
    SnapshotAvailableWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("RedshiftClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessToClusterDeniedFault: Type[BotocoreClientError]
    AccessToSnapshotDeniedFault: Type[BotocoreClientError]
    AuthenticationProfileAlreadyExistsFault: Type[BotocoreClientError]
    AuthenticationProfileNotFoundFault: Type[BotocoreClientError]
    AuthenticationProfileQuotaExceededFault: Type[BotocoreClientError]
    AuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    AuthorizationNotFoundFault: Type[BotocoreClientError]
    AuthorizationQuotaExceededFault: Type[BotocoreClientError]
    BatchDeleteRequestSizeExceededFault: Type[BotocoreClientError]
    BatchModifyClusterSnapshotsLimitExceededFault: Type[BotocoreClientError]
    BucketNotFoundFault: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ClusterAlreadyExistsFault: Type[BotocoreClientError]
    ClusterNotFoundFault: Type[BotocoreClientError]
    ClusterOnLatestRevisionFault: Type[BotocoreClientError]
    ClusterParameterGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterParameterGroupNotFoundFault: Type[BotocoreClientError]
    ClusterParameterGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterQuotaExceededFault: Type[BotocoreClientError]
    ClusterSecurityGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSecurityGroupNotFoundFault: Type[BotocoreClientError]
    ClusterSecurityGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterSnapshotAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSnapshotNotFoundFault: Type[BotocoreClientError]
    ClusterSnapshotQuotaExceededFault: Type[BotocoreClientError]
    ClusterSubnetGroupAlreadyExistsFault: Type[BotocoreClientError]
    ClusterSubnetGroupNotFoundFault: Type[BotocoreClientError]
    ClusterSubnetGroupQuotaExceededFault: Type[BotocoreClientError]
    ClusterSubnetQuotaExceededFault: Type[BotocoreClientError]
    ConflictPolicyUpdateFault: Type[BotocoreClientError]
    CopyToRegionDisabledFault: Type[BotocoreClientError]
    CustomCnameAssociationFault: Type[BotocoreClientError]
    CustomDomainAssociationNotFoundFault: Type[BotocoreClientError]
    DependentServiceAccessDeniedFault: Type[BotocoreClientError]
    DependentServiceRequestThrottlingFault: Type[BotocoreClientError]
    DependentServiceUnavailableFault: Type[BotocoreClientError]
    EndpointAlreadyExistsFault: Type[BotocoreClientError]
    EndpointAuthorizationAlreadyExistsFault: Type[BotocoreClientError]
    EndpointAuthorizationNotFoundFault: Type[BotocoreClientError]
    EndpointAuthorizationsPerClusterLimitExceededFault: Type[BotocoreClientError]
    EndpointNotFoundFault: Type[BotocoreClientError]
    EndpointsPerAuthorizationLimitExceededFault: Type[BotocoreClientError]
    EndpointsPerClusterLimitExceededFault: Type[BotocoreClientError]
    EventSubscriptionQuotaExceededFault: Type[BotocoreClientError]
    HsmClientCertificateAlreadyExistsFault: Type[BotocoreClientError]
    HsmClientCertificateNotFoundFault: Type[BotocoreClientError]
    HsmClientCertificateQuotaExceededFault: Type[BotocoreClientError]
    HsmConfigurationAlreadyExistsFault: Type[BotocoreClientError]
    HsmConfigurationNotFoundFault: Type[BotocoreClientError]
    HsmConfigurationQuotaExceededFault: Type[BotocoreClientError]
    InProgressTableRestoreQuotaExceededFault: Type[BotocoreClientError]
    IncompatibleOrderableOptions: Type[BotocoreClientError]
    InsufficientClusterCapacityFault: Type[BotocoreClientError]
    InsufficientS3BucketPolicyFault: Type[BotocoreClientError]
    IntegrationNotFoundFault: Type[BotocoreClientError]
    InvalidAuthenticationProfileRequestFault: Type[BotocoreClientError]
    InvalidAuthorizationStateFault: Type[BotocoreClientError]
    InvalidClusterParameterGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSecurityGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSnapshotScheduleStateFault: Type[BotocoreClientError]
    InvalidClusterSnapshotStateFault: Type[BotocoreClientError]
    InvalidClusterStateFault: Type[BotocoreClientError]
    InvalidClusterSubnetGroupStateFault: Type[BotocoreClientError]
    InvalidClusterSubnetStateFault: Type[BotocoreClientError]
    InvalidClusterTrackFault: Type[BotocoreClientError]
    InvalidDataShareFault: Type[BotocoreClientError]
    InvalidElasticIpFault: Type[BotocoreClientError]
    InvalidEndpointStateFault: Type[BotocoreClientError]
    InvalidHsmClientCertificateStateFault: Type[BotocoreClientError]
    InvalidHsmConfigurationStateFault: Type[BotocoreClientError]
    InvalidNamespaceFault: Type[BotocoreClientError]
    InvalidPolicyFault: Type[BotocoreClientError]
    InvalidReservedNodeStateFault: Type[BotocoreClientError]
    InvalidRestoreFault: Type[BotocoreClientError]
    InvalidRetentionPeriodFault: Type[BotocoreClientError]
    InvalidS3BucketNameFault: Type[BotocoreClientError]
    InvalidS3KeyPrefixFault: Type[BotocoreClientError]
    InvalidScheduleFault: Type[BotocoreClientError]
    InvalidScheduledActionFault: Type[BotocoreClientError]
    InvalidSnapshotCopyGrantStateFault: Type[BotocoreClientError]
    InvalidSubnet: Type[BotocoreClientError]
    InvalidSubscriptionStateFault: Type[BotocoreClientError]
    InvalidTableRestoreArgumentFault: Type[BotocoreClientError]
    InvalidTagFault: Type[BotocoreClientError]
    InvalidUsageLimitFault: Type[BotocoreClientError]
    InvalidVPCNetworkStateFault: Type[BotocoreClientError]
    Ipv6CidrBlockNotFoundFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    NumberOfNodesPerClusterLimitExceededFault: Type[BotocoreClientError]
    NumberOfNodesQuotaExceededFault: Type[BotocoreClientError]
    PartnerNotFoundFault: Type[BotocoreClientError]
    RedshiftIdcApplicationAlreadyExistsFault: Type[BotocoreClientError]
    RedshiftIdcApplicationNotExistsFault: Type[BotocoreClientError]
    RedshiftIdcApplicationQuotaExceededFault: Type[BotocoreClientError]
    ReservedNodeAlreadyExistsFault: Type[BotocoreClientError]
    ReservedNodeAlreadyMigratedFault: Type[BotocoreClientError]
    ReservedNodeExchangeNotFoundFault: Type[BotocoreClientError]
    ReservedNodeNotFoundFault: Type[BotocoreClientError]
    ReservedNodeOfferingNotFoundFault: Type[BotocoreClientError]
    ReservedNodeQuotaExceededFault: Type[BotocoreClientError]
    ResizeNotFoundFault: Type[BotocoreClientError]
    ResourceNotFoundFault: Type[BotocoreClientError]
    SNSInvalidTopicFault: Type[BotocoreClientError]
    SNSNoAuthorizationFault: Type[BotocoreClientError]
    SNSTopicArnNotFoundFault: Type[BotocoreClientError]
    ScheduleDefinitionTypeUnsupportedFault: Type[BotocoreClientError]
    ScheduledActionAlreadyExistsFault: Type[BotocoreClientError]
    ScheduledActionNotFoundFault: Type[BotocoreClientError]
    ScheduledActionQuotaExceededFault: Type[BotocoreClientError]
    ScheduledActionTypeUnsupportedFault: Type[BotocoreClientError]
    SnapshotCopyAlreadyDisabledFault: Type[BotocoreClientError]
    SnapshotCopyAlreadyEnabledFault: Type[BotocoreClientError]
    SnapshotCopyDisabledFault: Type[BotocoreClientError]
    SnapshotCopyGrantAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotCopyGrantNotFoundFault: Type[BotocoreClientError]
    SnapshotCopyGrantQuotaExceededFault: Type[BotocoreClientError]
    SnapshotScheduleAlreadyExistsFault: Type[BotocoreClientError]
    SnapshotScheduleNotFoundFault: Type[BotocoreClientError]
    SnapshotScheduleQuotaExceededFault: Type[BotocoreClientError]
    SnapshotScheduleUpdateInProgressFault: Type[BotocoreClientError]
    SourceNotFoundFault: Type[BotocoreClientError]
    SubnetAlreadyInUse: Type[BotocoreClientError]
    SubscriptionAlreadyExistFault: Type[BotocoreClientError]
    SubscriptionCategoryNotFoundFault: Type[BotocoreClientError]
    SubscriptionEventIdNotFoundFault: Type[BotocoreClientError]
    SubscriptionNotFoundFault: Type[BotocoreClientError]
    SubscriptionSeverityNotFoundFault: Type[BotocoreClientError]
    TableLimitExceededFault: Type[BotocoreClientError]
    TableRestoreNotFoundFault: Type[BotocoreClientError]
    TagLimitExceededFault: Type[BotocoreClientError]
    UnauthorizedOperation: Type[BotocoreClientError]
    UnauthorizedPartnerIntegrationFault: Type[BotocoreClientError]
    UnknownSnapshotCopyRegionFault: Type[BotocoreClientError]
    UnsupportedOperationFault: Type[BotocoreClientError]
    UnsupportedOptionFault: Type[BotocoreClientError]
    UsageLimitAlreadyExistsFault: Type[BotocoreClientError]
    UsageLimitNotFoundFault: Type[BotocoreClientError]


class RedshiftClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RedshiftClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#exceptions)
        """

    async def accept_reserved_node_exchange(
        self, *, ReservedNodeId: str, TargetReservedNodeOfferingId: str
    ) -> AcceptReservedNodeExchangeOutputMessageTypeDef:
        """
        Exchanges a DC1 Reserved Node for a DC2 Reserved Node with no changes to the
        configuration (term, payment type, or number of nodes) and no additional
        costs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.accept_reserved_node_exchange)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#accept_reserved_node_exchange)
        """

    async def add_partner(
        self, *, AccountId: str, ClusterIdentifier: str, DatabaseName: str, PartnerName: str
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Adds a partner integration to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.add_partner)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#add_partner)
        """

    async def associate_data_share_consumer(
        self,
        *,
        DataShareArn: str,
        AssociateEntireAccount: bool = ...,
        ConsumerArn: str = ...,
        ConsumerRegion: str = ...,
        AllowWrites: bool = ...,
    ) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, associates a datashare with the account
        (AssociateEntireAccount) or the specified namespace
        (ConsumerArn).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.associate_data_share_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#associate_data_share_consumer)
        """

    async def authorize_cluster_security_group_ingress(
        self,
        *,
        ClusterSecurityGroupName: str,
        CIDRIP: str = ...,
        EC2SecurityGroupName: str = ...,
        EC2SecurityGroupOwnerId: str = ...,
    ) -> AuthorizeClusterSecurityGroupIngressResultTypeDef:
        """
        Adds an inbound (ingress) rule to an Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.authorize_cluster_security_group_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#authorize_cluster_security_group_ingress)
        """

    async def authorize_data_share(
        self, *, DataShareArn: str, ConsumerIdentifier: str, AllowWrites: bool = ...
    ) -> DataShareResponseTypeDef:
        """
        From a data producer account, authorizes the sharing of a datashare with one or
        more consumer accounts or managing
        entities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.authorize_data_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#authorize_data_share)
        """

    async def authorize_endpoint_access(
        self, *, Account: str, ClusterIdentifier: str = ..., VpcIds: Sequence[str] = ...
    ) -> EndpointAuthorizationResponseTypeDef:
        """
        Grants access to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.authorize_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#authorize_endpoint_access)
        """

    async def authorize_snapshot_access(
        self,
        *,
        AccountWithRestoreAccess: str,
        SnapshotIdentifier: str = ...,
        SnapshotArn: str = ...,
        SnapshotClusterIdentifier: str = ...,
    ) -> AuthorizeSnapshotAccessResultTypeDef:
        """
        Authorizes the specified Amazon Web Services account to restore the specified
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.authorize_snapshot_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#authorize_snapshot_access)
        """

    async def batch_delete_cluster_snapshots(
        self, *, Identifiers: Sequence[DeleteClusterSnapshotMessageTypeDef]
    ) -> BatchDeleteClusterSnapshotsResultTypeDef:
        """
        Deletes a set of cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.batch_delete_cluster_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#batch_delete_cluster_snapshots)
        """

    async def batch_modify_cluster_snapshots(
        self,
        *,
        SnapshotIdentifierList: Sequence[str],
        ManualSnapshotRetentionPeriod: int = ...,
        Force: bool = ...,
    ) -> BatchModifyClusterSnapshotsOutputMessageTypeDef:
        """
        Modifies the settings for a set of cluster snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.batch_modify_cluster_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#batch_modify_cluster_snapshots)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#can_paginate)
        """

    async def cancel_resize(self, *, ClusterIdentifier: str) -> ResizeProgressMessageTypeDef:
        """
        Cancels a resize operation for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.cancel_resize)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#cancel_resize)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#close)
        """

    async def copy_cluster_snapshot(
        self,
        *,
        SourceSnapshotIdentifier: str,
        TargetSnapshotIdentifier: str,
        SourceSnapshotClusterIdentifier: str = ...,
        ManualSnapshotRetentionPeriod: int = ...,
    ) -> CopyClusterSnapshotResultTypeDef:
        """
        Copies the specified automated cluster snapshot to a new manual cluster
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.copy_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#copy_cluster_snapshot)
        """

    async def create_authentication_profile(
        self, *, AuthenticationProfileName: str, AuthenticationProfileContent: str
    ) -> CreateAuthenticationProfileResultTypeDef:
        """
        Creates an authentication profile with the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_authentication_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_authentication_profile)
        """

    async def create_cluster(
        self,
        *,
        ClusterIdentifier: str,
        NodeType: str,
        MasterUsername: str,
        DBName: str = ...,
        ClusterType: str = ...,
        MasterUserPassword: str = ...,
        ClusterSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        ClusterSubnetGroupName: str = ...,
        AvailabilityZone: str = ...,
        PreferredMaintenanceWindow: str = ...,
        ClusterParameterGroupName: str = ...,
        AutomatedSnapshotRetentionPeriod: int = ...,
        ManualSnapshotRetentionPeriod: int = ...,
        Port: int = ...,
        ClusterVersion: str = ...,
        AllowVersionUpgrade: bool = ...,
        NumberOfNodes: int = ...,
        PubliclyAccessible: bool = ...,
        Encrypted: bool = ...,
        HsmClientCertificateIdentifier: str = ...,
        HsmConfigurationIdentifier: str = ...,
        ElasticIp: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        EnhancedVpcRouting: bool = ...,
        AdditionalInfo: str = ...,
        IamRoles: Sequence[str] = ...,
        MaintenanceTrackName: str = ...,
        SnapshotScheduleIdentifier: str = ...,
        AvailabilityZoneRelocation: bool = ...,
        AquaConfigurationStatus: AquaConfigurationStatusType = ...,
        DefaultIamRoleArn: str = ...,
        LoadSampleData: str = ...,
        ManageMasterPassword: bool = ...,
        MasterPasswordSecretKmsKeyId: str = ...,
        IpAddressType: str = ...,
        MultiAZ: bool = ...,
        RedshiftIdcApplicationArn: str = ...,
    ) -> CreateClusterResultTypeDef:
        """
        Creates a new cluster with the specified parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_cluster)
        """

    async def create_cluster_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        ParameterGroupFamily: str,
        Description: str,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateClusterParameterGroupResultTypeDef:
        """
        Creates an Amazon Redshift parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_cluster_parameter_group)
        """

    async def create_cluster_security_group(
        self, *, ClusterSecurityGroupName: str, Description: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateClusterSecurityGroupResultTypeDef:
        """
        Creates a new Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_cluster_security_group)
        """

    async def create_cluster_snapshot(
        self,
        *,
        SnapshotIdentifier: str,
        ClusterIdentifier: str,
        ManualSnapshotRetentionPeriod: int = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateClusterSnapshotResultTypeDef:
        """
        Creates a manual snapshot of the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_cluster_snapshot)
        """

    async def create_cluster_subnet_group(
        self,
        *,
        ClusterSubnetGroupName: str,
        Description: str,
        SubnetIds: Sequence[str],
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateClusterSubnetGroupResultTypeDef:
        """
        Creates a new Amazon Redshift subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_cluster_subnet_group)
        """

    async def create_custom_domain_association(
        self, *, CustomDomainName: str, CustomDomainCertificateArn: str, ClusterIdentifier: str
    ) -> CreateCustomDomainAssociationResultTypeDef:
        """
        Used to create a custom domain name for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_custom_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_custom_domain_association)
        """

    async def create_endpoint_access(
        self,
        *,
        EndpointName: str,
        SubnetGroupName: str,
        ClusterIdentifier: str = ...,
        ResourceOwner: str = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
    ) -> EndpointAccessResponseTypeDef:
        """
        Creates a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_endpoint_access)
        """

    async def create_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str,
        SourceType: str = ...,
        SourceIds: Sequence[str] = ...,
        EventCategories: Sequence[str] = ...,
        Severity: str = ...,
        Enabled: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateEventSubscriptionResultTypeDef:
        """
        Creates an Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_event_subscription)
        """

    async def create_hsm_client_certificate(
        self, *, HsmClientCertificateIdentifier: str, Tags: Sequence[TagTypeDef] = ...
    ) -> CreateHsmClientCertificateResultTypeDef:
        """
        Creates an HSM client certificate that an Amazon Redshift cluster will use to
        connect to the client's HSM in order to store and retrieve the keys used to
        encrypt the cluster
        databases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_hsm_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_hsm_client_certificate)
        """

    async def create_hsm_configuration(
        self,
        *,
        HsmConfigurationIdentifier: str,
        Description: str,
        HsmIpAddress: str,
        HsmPartitionName: str,
        HsmPartitionPassword: str,
        HsmServerPublicCertificate: str,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateHsmConfigurationResultTypeDef:
        """
        Creates an HSM configuration that contains the information required by an
        Amazon Redshift cluster to store and use database encryption keys in a Hardware
        Security Module
        (HSM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_hsm_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_hsm_configuration)
        """

    async def create_redshift_idc_application(
        self,
        *,
        IdcInstanceArn: str,
        RedshiftIdcApplicationName: str,
        IdcDisplayName: str,
        IamRoleArn: str,
        IdentityNamespace: str = ...,
        AuthorizedTokenIssuerList: Sequence[AuthorizedTokenIssuerUnionTypeDef] = ...,
        ServiceIntegrations: Sequence[ServiceIntegrationsUnionUnionTypeDef] = ...,
    ) -> CreateRedshiftIdcApplicationResultTypeDef:
        """
        Creates an Amazon Redshift application for use with IAM Identity Center.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_redshift_idc_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_redshift_idc_application)
        """

    async def create_scheduled_action(
        self,
        *,
        ScheduledActionName: str,
        TargetAction: ScheduledActionTypeTypeDef,
        Schedule: str,
        IamRole: str,
        ScheduledActionDescription: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        Enable: bool = ...,
    ) -> ScheduledActionResponseTypeDef:
        """
        Creates a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_scheduled_action)
        """

    async def create_snapshot_copy_grant(
        self, *, SnapshotCopyGrantName: str, KmsKeyId: str = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> CreateSnapshotCopyGrantResultTypeDef:
        """
        Creates a snapshot copy grant that permits Amazon Redshift to use an encrypted
        symmetric key from Key Management Service (KMS) to encrypt copied snapshots in
        a destination
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_snapshot_copy_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_snapshot_copy_grant)
        """

    async def create_snapshot_schedule(
        self,
        *,
        ScheduleDefinitions: Sequence[str] = ...,
        ScheduleIdentifier: str = ...,
        ScheduleDescription: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        DryRun: bool = ...,
        NextInvocations: int = ...,
    ) -> SnapshotScheduleResponseTypeDef:
        """
        Create a snapshot schedule that can be associated to a cluster and which
        overrides the default system backup
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_snapshot_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_snapshot_schedule)
        """

    async def create_tags(
        self, *, ResourceName: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_tags)
        """

    async def create_usage_limit(
        self,
        *,
        ClusterIdentifier: str,
        FeatureType: UsageLimitFeatureTypeType,
        LimitType: UsageLimitLimitTypeType,
        Amount: int,
        Period: UsageLimitPeriodType = ...,
        BreachAction: UsageLimitBreachActionType = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> UsageLimitResponseTypeDef:
        """
        Creates a usage limit for a specified Amazon Redshift feature on a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_usage_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#create_usage_limit)
        """

    async def deauthorize_data_share(
        self, *, DataShareArn: str, ConsumerIdentifier: str
    ) -> DataShareResponseTypeDef:
        """
        From a datashare producer account, removes authorization from the specified
        datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.deauthorize_data_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#deauthorize_data_share)
        """

    async def delete_authentication_profile(
        self, *, AuthenticationProfileName: str
    ) -> DeleteAuthenticationProfileResultTypeDef:
        """
        Deletes an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_authentication_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_authentication_profile)
        """

    async def delete_cluster(
        self,
        *,
        ClusterIdentifier: str,
        SkipFinalClusterSnapshot: bool = ...,
        FinalClusterSnapshotIdentifier: str = ...,
        FinalClusterSnapshotRetentionPeriod: int = ...,
    ) -> DeleteClusterResultTypeDef:
        """
        Deletes a previously provisioned cluster without its final snapshot being
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_cluster)
        """

    async def delete_cluster_parameter_group(
        self, *, ParameterGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specified Amazon Redshift parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_cluster_parameter_group)
        """

    async def delete_cluster_security_group(
        self, *, ClusterSecurityGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift security group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_cluster_security_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_cluster_security_group)
        """

    async def delete_cluster_snapshot(
        self, *, SnapshotIdentifier: str, SnapshotClusterIdentifier: str = ...
    ) -> DeleteClusterSnapshotResultTypeDef:
        """
        Deletes the specified manual snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_cluster_snapshot)
        """

    async def delete_cluster_subnet_group(
        self, *, ClusterSubnetGroupName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified cluster subnet group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_cluster_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_cluster_subnet_group)
        """

    async def delete_custom_domain_association(
        self, *, ClusterIdentifier: str, CustomDomainName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Contains information about deleting a custom domain association for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_custom_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_custom_domain_association)
        """

    async def delete_endpoint_access(self, *, EndpointName: str) -> EndpointAccessResponseTypeDef:
        """
        Deletes a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_endpoint_access)
        """

    async def delete_event_subscription(
        self, *, SubscriptionName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_event_subscription)
        """

    async def delete_hsm_client_certificate(
        self, *, HsmClientCertificateIdentifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified HSM client certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_hsm_client_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_hsm_client_certificate)
        """

    async def delete_hsm_configuration(
        self, *, HsmConfigurationIdentifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified Amazon Redshift HSM configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_hsm_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_hsm_configuration)
        """

    async def delete_partner(
        self, *, AccountId: str, ClusterIdentifier: str, DatabaseName: str, PartnerName: str
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Deletes a partner integration from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_partner)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_partner)
        """

    async def delete_redshift_idc_application(
        self, *, RedshiftIdcApplicationArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Redshift IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_redshift_idc_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_redshift_idc_application)
        """

    async def delete_resource_policy(self, *, ResourceArn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_resource_policy)
        """

    async def delete_scheduled_action(
        self, *, ScheduledActionName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_scheduled_action)
        """

    async def delete_snapshot_copy_grant(
        self, *, SnapshotCopyGrantName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified snapshot copy grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_snapshot_copy_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_snapshot_copy_grant)
        """

    async def delete_snapshot_schedule(
        self, *, ScheduleIdentifier: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a snapshot schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_snapshot_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_snapshot_schedule)
        """

    async def delete_tags(
        self, *, ResourceName: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_tags)
        """

    async def delete_usage_limit(self, *, UsageLimitId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a usage limit from a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.delete_usage_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#delete_usage_limit)
        """

    async def describe_account_attributes(
        self, *, AttributeNames: Sequence[str] = ...
    ) -> AccountAttributeListTypeDef:
        """
        Returns a list of attributes attached to an account See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/redshift-2012-12-01/DescribeAccountAttributes).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_account_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_account_attributes)
        """

    async def describe_authentication_profiles(
        self, *, AuthenticationProfileName: str = ...
    ) -> DescribeAuthenticationProfilesResultTypeDef:
        """
        Describes an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_authentication_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_authentication_profiles)
        """

    async def describe_cluster_db_revisions(
        self, *, ClusterIdentifier: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> ClusterDbRevisionsMessageTypeDef:
        """
        Returns an array of `ClusterDbRevision` objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_db_revisions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_db_revisions)
        """

    async def describe_cluster_parameter_groups(
        self,
        *,
        ParameterGroupName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> ClusterParameterGroupsMessageTypeDef:
        """
        Returns a list of Amazon Redshift parameter groups, including parameter groups
        you created and the default parameter
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_parameter_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_parameter_groups)
        """

    async def describe_cluster_parameters(
        self,
        *,
        ParameterGroupName: str,
        Source: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ClusterParameterGroupDetailsTypeDef:
        """
        Returns a detailed list of parameters contained within the specified Amazon
        Redshift parameter
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_parameters)
        """

    async def describe_cluster_security_groups(
        self,
        *,
        ClusterSecurityGroupName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> ClusterSecurityGroupMessageTypeDef:
        """
        Returns information about Amazon Redshift security groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_security_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_security_groups)
        """

    async def describe_cluster_snapshots(
        self,
        *,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        SnapshotArn: str = ...,
        SnapshotType: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        OwnerAccount: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        ClusterExists: bool = ...,
        SortingEntities: Sequence[SnapshotSortingEntityTypeDef] = ...,
    ) -> SnapshotMessageTypeDef:
        """
        Returns one or more snapshot objects, which contain metadata about your cluster
        snapshots.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_snapshots)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_snapshots)
        """

    async def describe_cluster_subnet_groups(
        self,
        *,
        ClusterSubnetGroupName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> ClusterSubnetGroupMessageTypeDef:
        """
        Returns one or more cluster subnet group objects, which contain metadata about
        your cluster subnet
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_subnet_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_subnet_groups)
        """

    async def describe_cluster_tracks(
        self, *, MaintenanceTrackName: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> TrackListMessageTypeDef:
        """
        Returns a list of all the available maintenance tracks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_tracks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_tracks)
        """

    async def describe_cluster_versions(
        self,
        *,
        ClusterVersion: str = ...,
        ClusterParameterGroupFamily: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ClusterVersionsMessageTypeDef:
        """
        Returns descriptions of the available Amazon Redshift cluster versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_cluster_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_cluster_versions)
        """

    async def describe_clusters(
        self,
        *,
        ClusterIdentifier: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> ClustersMessageTypeDef:
        """
        Returns properties of provisioned clusters including general cluster
        properties, cluster database properties, maintenance and backup properties, and
        security and access
        properties.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_clusters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_clusters)
        """

    async def describe_custom_domain_associations(
        self,
        *,
        CustomDomainName: str = ...,
        CustomDomainCertificateArn: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> CustomDomainAssociationsMessageTypeDef:
        """
        Contains information about custom domain associations for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_custom_domain_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_custom_domain_associations)
        """

    async def describe_data_shares(
        self, *, DataShareArn: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeDataSharesResultTypeDef:
        """
        Shows the status of any inbound or outbound datashares available in the
        specified
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_data_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_data_shares)
        """

    async def describe_data_shares_for_consumer(
        self,
        *,
        ConsumerArn: str = ...,
        Status: DataShareStatusForConsumerType = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> DescribeDataSharesForConsumerResultTypeDef:
        """
        Returns a list of datashares where the account identifier being called is a
        consumer account
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_data_shares_for_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_data_shares_for_consumer)
        """

    async def describe_data_shares_for_producer(
        self,
        *,
        ProducerArn: str = ...,
        Status: DataShareStatusForProducerType = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> DescribeDataSharesForProducerResultTypeDef:
        """
        Returns a list of datashares when the account identifier being called is a
        producer account
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_data_shares_for_producer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_data_shares_for_producer)
        """

    async def describe_default_cluster_parameters(
        self, *, ParameterGroupFamily: str, MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeDefaultClusterParametersResultTypeDef:
        """
        Returns a list of parameter settings for the specified parameter group family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_default_cluster_parameters)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_default_cluster_parameters)
        """

    async def describe_endpoint_access(
        self,
        *,
        ClusterIdentifier: str = ...,
        ResourceOwner: str = ...,
        EndpointName: str = ...,
        VpcId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> EndpointAccessListTypeDef:
        """
        Describes a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_endpoint_access)
        """

    async def describe_endpoint_authorization(
        self,
        *,
        ClusterIdentifier: str = ...,
        Account: str = ...,
        Grantee: bool = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> EndpointAuthorizationListTypeDef:
        """
        Describes an endpoint authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_endpoint_authorization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_endpoint_authorization)
        """

    async def describe_event_categories(
        self, *, SourceType: str = ...
    ) -> EventCategoriesMessageTypeDef:
        """
        Displays a list of event categories for all event source types, or for a
        specified source
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_event_categories)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_event_categories)
        """

    async def describe_event_subscriptions(
        self,
        *,
        SubscriptionName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> EventSubscriptionsMessageTypeDef:
        """
        Lists descriptions of all the Amazon Redshift event notification subscriptions
        for a customer
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_event_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_event_subscriptions)
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
        Returns events related to clusters, security groups, snapshots, and parameter
        groups for the past 14
        days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_events)
        """

    async def describe_hsm_client_certificates(
        self,
        *,
        HsmClientCertificateIdentifier: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> HsmClientCertificateMessageTypeDef:
        """
        Returns information about the specified HSM client certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_hsm_client_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_hsm_client_certificates)
        """

    async def describe_hsm_configurations(
        self,
        *,
        HsmConfigurationIdentifier: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> HsmConfigurationMessageTypeDef:
        """
        Returns information about the specified Amazon Redshift HSM configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_hsm_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_hsm_configurations)
        """

    async def describe_inbound_integrations(
        self,
        *,
        IntegrationArn: str = ...,
        TargetArn: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> InboundIntegrationsMessageTypeDef:
        """
        Returns a list of inbound integrations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_inbound_integrations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_inbound_integrations)
        """

    async def describe_logging_status(self, *, ClusterIdentifier: str) -> LoggingStatusTypeDef:
        """
        Describes whether information, such as queries and connection attempts, is
        being logged for the specified Amazon Redshift
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_logging_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_logging_status)
        """

    async def describe_node_configuration_options(
        self,
        *,
        ActionType: ActionTypeType,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        SnapshotArn: str = ...,
        OwnerAccount: str = ...,
        Filters: Sequence[NodeConfigurationOptionsFilterTypeDef] = ...,
        Marker: str = ...,
        MaxRecords: int = ...,
    ) -> NodeConfigurationOptionsMessageTypeDef:
        """
        Returns properties of possible node configurations such as node type, number of
        nodes, and disk usage for the specified action
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_node_configuration_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_node_configuration_options)
        """

    async def describe_orderable_cluster_options(
        self,
        *,
        ClusterVersion: str = ...,
        NodeType: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> OrderableClusterOptionsMessageTypeDef:
        """
        Returns a list of orderable cluster options.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_orderable_cluster_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_orderable_cluster_options)
        """

    async def describe_partners(
        self,
        *,
        AccountId: str,
        ClusterIdentifier: str,
        DatabaseName: str = ...,
        PartnerName: str = ...,
    ) -> DescribePartnersOutputMessageTypeDef:
        """
        Returns information about the partner integrations defined for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_partners)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_partners)
        """

    async def describe_redshift_idc_applications(
        self, *, RedshiftIdcApplicationArn: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> DescribeRedshiftIdcApplicationsResultTypeDef:
        """
        Lists the Amazon Redshift IAM Identity Center applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_redshift_idc_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_redshift_idc_applications)
        """

    async def describe_reserved_node_exchange_status(
        self,
        *,
        ReservedNodeId: str = ...,
        ReservedNodeExchangeRequestId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> DescribeReservedNodeExchangeStatusOutputMessageTypeDef:
        """
        Returns exchange status details and associated metadata for a reserved-node
        exchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_reserved_node_exchange_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_reserved_node_exchange_status)
        """

    async def describe_reserved_node_offerings(
        self, *, ReservedNodeOfferingId: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> ReservedNodeOfferingsMessageTypeDef:
        """
        Returns a list of the available reserved node offerings by Amazon Redshift with
        their descriptions including the node type, the fixed and recurring costs of
        reserving the node and duration the node will be reserved for
        you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_reserved_node_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_reserved_node_offerings)
        """

    async def describe_reserved_nodes(
        self, *, ReservedNodeId: str = ..., MaxRecords: int = ..., Marker: str = ...
    ) -> ReservedNodesMessageTypeDef:
        """
        Returns the descriptions of the reserved nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_reserved_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_reserved_nodes)
        """

    async def describe_resize(self, *, ClusterIdentifier: str) -> ResizeProgressMessageTypeDef:
        """
        Returns information about the last resize operation for the specified cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_resize)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_resize)
        """

    async def describe_scheduled_actions(
        self,
        *,
        ScheduledActionName: str = ...,
        TargetActionType: ScheduledActionTypeValuesType = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        Active: bool = ...,
        Filters: Sequence[ScheduledActionFilterTypeDef] = ...,
        Marker: str = ...,
        MaxRecords: int = ...,
    ) -> ScheduledActionsMessageTypeDef:
        """
        Describes properties of scheduled actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_scheduled_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_scheduled_actions)
        """

    async def describe_snapshot_copy_grants(
        self,
        *,
        SnapshotCopyGrantName: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> SnapshotCopyGrantMessageTypeDef:
        """
        Returns a list of snapshot copy grants owned by the Amazon Web Services account
        in the destination
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_snapshot_copy_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_snapshot_copy_grants)
        """

    async def describe_snapshot_schedules(
        self,
        *,
        ClusterIdentifier: str = ...,
        ScheduleIdentifier: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
        Marker: str = ...,
        MaxRecords: int = ...,
    ) -> DescribeSnapshotSchedulesOutputMessageTypeDef:
        """
        Returns a list of snapshot schedules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_snapshot_schedules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_snapshot_schedules)
        """

    async def describe_storage(self) -> CustomerStorageMessageTypeDef:
        """
        Returns account level backups storage size and provisional storage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_storage)
        """

    async def describe_table_restore_status(
        self,
        *,
        ClusterIdentifier: str = ...,
        TableRestoreRequestId: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> TableRestoreStatusMessageTypeDef:
        """
        Lists the status of one or more table restore requests made using the
        RestoreTableFromClusterSnapshot API
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_table_restore_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_table_restore_status)
        """

    async def describe_tags(
        self,
        *,
        ResourceName: str = ...,
        ResourceType: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> TaggedResourceListMessageTypeDef:
        """
        Returns a list of tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_tags)
        """

    async def describe_usage_limits(
        self,
        *,
        UsageLimitId: str = ...,
        ClusterIdentifier: str = ...,
        FeatureType: UsageLimitFeatureTypeType = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
        TagKeys: Sequence[str] = ...,
        TagValues: Sequence[str] = ...,
    ) -> UsageLimitListTypeDef:
        """
        Shows usage limits on a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.describe_usage_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#describe_usage_limits)
        """

    async def disable_logging(self, *, ClusterIdentifier: str) -> LoggingStatusTypeDef:
        """
        Stops logging information, such as queries and connection attempts, for the
        specified Amazon Redshift
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.disable_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#disable_logging)
        """

    async def disable_snapshot_copy(
        self, *, ClusterIdentifier: str
    ) -> DisableSnapshotCopyResultTypeDef:
        """
        Disables the automatic copying of snapshots from one region to another region
        for a specified
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.disable_snapshot_copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#disable_snapshot_copy)
        """

    async def disassociate_data_share_consumer(
        self,
        *,
        DataShareArn: str,
        DisassociateEntireAccount: bool = ...,
        ConsumerArn: str = ...,
        ConsumerRegion: str = ...,
    ) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, remove association for the specified
        datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.disassociate_data_share_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#disassociate_data_share_consumer)
        """

    async def enable_logging(
        self,
        *,
        ClusterIdentifier: str,
        BucketName: str = ...,
        S3KeyPrefix: str = ...,
        LogDestinationType: LogDestinationTypeType = ...,
        LogExports: Sequence[str] = ...,
    ) -> LoggingStatusTypeDef:
        """
        Starts logging information, such as queries and connection attempts, for the
        specified Amazon Redshift
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.enable_logging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#enable_logging)
        """

    async def enable_snapshot_copy(
        self,
        *,
        ClusterIdentifier: str,
        DestinationRegion: str,
        RetentionPeriod: int = ...,
        SnapshotCopyGrantName: str = ...,
        ManualSnapshotRetentionPeriod: int = ...,
    ) -> EnableSnapshotCopyResultTypeDef:
        """
        Enables the automatic copy of snapshots from one region to another region for a
        specified
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.enable_snapshot_copy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#enable_snapshot_copy)
        """

    async def failover_primary_compute(
        self, *, ClusterIdentifier: str
    ) -> FailoverPrimaryComputeResultTypeDef:
        """
        Fails over the primary compute unit of the specified Multi-AZ cluster to
        another Availability
        Zone.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.failover_primary_compute)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#failover_primary_compute)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#generate_presigned_url)
        """

    async def get_cluster_credentials(
        self,
        *,
        DbUser: str,
        DbName: str = ...,
        ClusterIdentifier: str = ...,
        DurationSeconds: int = ...,
        AutoCreate: bool = ...,
        DbGroups: Sequence[str] = ...,
        CustomDomainName: str = ...,
    ) -> ClusterCredentialsTypeDef:
        """
        Returns a database user name and temporary password with temporary
        authorization to log on to an Amazon Redshift
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_cluster_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_cluster_credentials)
        """

    async def get_cluster_credentials_with_iam(
        self,
        *,
        DbName: str = ...,
        ClusterIdentifier: str = ...,
        DurationSeconds: int = ...,
        CustomDomainName: str = ...,
    ) -> ClusterExtendedCredentialsTypeDef:
        """
        Returns a database user name and temporary password with temporary
        authorization to log in to an Amazon Redshift
        database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_cluster_credentials_with_iam)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_cluster_credentials_with_iam)
        """

    async def get_reserved_node_exchange_configuration_options(
        self,
        *,
        ActionType: ReservedNodeExchangeActionTypeType,
        ClusterIdentifier: str = ...,
        SnapshotIdentifier: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> GetReservedNodeExchangeConfigurationOptionsOutputMessageTypeDef:
        """
        Gets the configuration options for the reserved-node exchange.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_reserved_node_exchange_configuration_options)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_reserved_node_exchange_configuration_options)
        """

    async def get_reserved_node_exchange_offerings(
        self, *, ReservedNodeId: str, MaxRecords: int = ..., Marker: str = ...
    ) -> GetReservedNodeExchangeOfferingsOutputMessageTypeDef:
        """
        Returns an array of DC2 ReservedNodeOfferings that matches the payment type,
        term, and usage price of the given DC1 reserved
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_reserved_node_exchange_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_reserved_node_exchange_offerings)
        """

    async def get_resource_policy(self, *, ResourceArn: str) -> GetResourcePolicyResultTypeDef:
        """
        Get the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_resource_policy)
        """

    async def list_recommendations(
        self,
        *,
        ClusterIdentifier: str = ...,
        NamespaceArn: str = ...,
        MaxRecords: int = ...,
        Marker: str = ...,
    ) -> ListRecommendationsResultTypeDef:
        """
        List the Amazon Redshift Advisor recommendations for one or multiple Amazon
        Redshift clusters in an Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.list_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#list_recommendations)
        """

    async def modify_aqua_configuration(
        self, *, ClusterIdentifier: str, AquaConfigurationStatus: AquaConfigurationStatusType = ...
    ) -> ModifyAquaOutputMessageTypeDef:
        """
        This operation is retired.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_aqua_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_aqua_configuration)
        """

    async def modify_authentication_profile(
        self, *, AuthenticationProfileName: str, AuthenticationProfileContent: str
    ) -> ModifyAuthenticationProfileResultTypeDef:
        """
        Modifies an authentication profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_authentication_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_authentication_profile)
        """

    async def modify_cluster(
        self,
        *,
        ClusterIdentifier: str,
        ClusterType: str = ...,
        NodeType: str = ...,
        NumberOfNodes: int = ...,
        ClusterSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        MasterUserPassword: str = ...,
        ClusterParameterGroupName: str = ...,
        AutomatedSnapshotRetentionPeriod: int = ...,
        ManualSnapshotRetentionPeriod: int = ...,
        PreferredMaintenanceWindow: str = ...,
        ClusterVersion: str = ...,
        AllowVersionUpgrade: bool = ...,
        HsmClientCertificateIdentifier: str = ...,
        HsmConfigurationIdentifier: str = ...,
        NewClusterIdentifier: str = ...,
        PubliclyAccessible: bool = ...,
        ElasticIp: str = ...,
        EnhancedVpcRouting: bool = ...,
        MaintenanceTrackName: str = ...,
        Encrypted: bool = ...,
        KmsKeyId: str = ...,
        AvailabilityZoneRelocation: bool = ...,
        AvailabilityZone: str = ...,
        Port: int = ...,
        ManageMasterPassword: bool = ...,
        MasterPasswordSecretKmsKeyId: str = ...,
        IpAddressType: str = ...,
        MultiAZ: bool = ...,
    ) -> ModifyClusterResultTypeDef:
        """
        Modifies the settings for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster)
        """

    async def modify_cluster_db_revision(
        self, *, ClusterIdentifier: str, RevisionTarget: str
    ) -> ModifyClusterDbRevisionResultTypeDef:
        """
        Modifies the database revision of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_db_revision)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_db_revision)
        """

    async def modify_cluster_iam_roles(
        self,
        *,
        ClusterIdentifier: str,
        AddIamRoles: Sequence[str] = ...,
        RemoveIamRoles: Sequence[str] = ...,
        DefaultIamRoleArn: str = ...,
    ) -> ModifyClusterIamRolesResultTypeDef:
        """
        Modifies the list of Identity and Access Management (IAM) roles that can be
        used by the cluster to access other Amazon Web Services
        services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_iam_roles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_iam_roles)
        """

    async def modify_cluster_maintenance(
        self,
        *,
        ClusterIdentifier: str,
        DeferMaintenance: bool = ...,
        DeferMaintenanceIdentifier: str = ...,
        DeferMaintenanceStartTime: TimestampTypeDef = ...,
        DeferMaintenanceEndTime: TimestampTypeDef = ...,
        DeferMaintenanceDuration: int = ...,
    ) -> ModifyClusterMaintenanceResultTypeDef:
        """
        Modifies the maintenance settings of a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_maintenance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_maintenance)
        """

    async def modify_cluster_parameter_group(
        self, *, ParameterGroupName: str, Parameters: Sequence[ParameterTypeDef]
    ) -> ClusterParameterGroupNameMessageTypeDef:
        """
        Modifies the parameters of a parameter group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_parameter_group)
        """

    async def modify_cluster_snapshot(
        self,
        *,
        SnapshotIdentifier: str,
        ManualSnapshotRetentionPeriod: int = ...,
        Force: bool = ...,
    ) -> ModifyClusterSnapshotResultTypeDef:
        """
        Modifies the settings for a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_snapshot)
        """

    async def modify_cluster_snapshot_schedule(
        self,
        *,
        ClusterIdentifier: str,
        ScheduleIdentifier: str = ...,
        DisassociateSchedule: bool = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies a snapshot schedule for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_snapshot_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_snapshot_schedule)
        """

    async def modify_cluster_subnet_group(
        self, *, ClusterSubnetGroupName: str, SubnetIds: Sequence[str], Description: str = ...
    ) -> ModifyClusterSubnetGroupResultTypeDef:
        """
        Modifies a cluster subnet group to include the specified list of VPC subnets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_cluster_subnet_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_cluster_subnet_group)
        """

    async def modify_custom_domain_association(
        self, *, CustomDomainName: str, CustomDomainCertificateArn: str, ClusterIdentifier: str
    ) -> ModifyCustomDomainAssociationResultTypeDef:
        """
        Contains information for changing a custom domain association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_custom_domain_association)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_custom_domain_association)
        """

    async def modify_endpoint_access(
        self, *, EndpointName: str, VpcSecurityGroupIds: Sequence[str] = ...
    ) -> EndpointAccessResponseTypeDef:
        """
        Modifies a Redshift-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_endpoint_access)
        """

    async def modify_event_subscription(
        self,
        *,
        SubscriptionName: str,
        SnsTopicArn: str = ...,
        SourceType: str = ...,
        SourceIds: Sequence[str] = ...,
        EventCategories: Sequence[str] = ...,
        Severity: str = ...,
        Enabled: bool = ...,
    ) -> ModifyEventSubscriptionResultTypeDef:
        """
        Modifies an existing Amazon Redshift event notification subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_event_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_event_subscription)
        """

    async def modify_redshift_idc_application(
        self,
        *,
        RedshiftIdcApplicationArn: str,
        IdentityNamespace: str = ...,
        IamRoleArn: str = ...,
        IdcDisplayName: str = ...,
        AuthorizedTokenIssuerList: Sequence[AuthorizedTokenIssuerUnionTypeDef] = ...,
        ServiceIntegrations: Sequence[ServiceIntegrationsUnionUnionTypeDef] = ...,
    ) -> ModifyRedshiftIdcApplicationResultTypeDef:
        """
        Changes an existing Amazon Redshift IAM Identity Center application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_redshift_idc_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_redshift_idc_application)
        """

    async def modify_scheduled_action(
        self,
        *,
        ScheduledActionName: str,
        TargetAction: ScheduledActionTypeTypeDef = ...,
        Schedule: str = ...,
        IamRole: str = ...,
        ScheduledActionDescription: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        Enable: bool = ...,
    ) -> ScheduledActionResponseTypeDef:
        """
        Modifies a scheduled action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_scheduled_action)
        """

    async def modify_snapshot_copy_retention_period(
        self, *, ClusterIdentifier: str, RetentionPeriod: int, Manual: bool = ...
    ) -> ModifySnapshotCopyRetentionPeriodResultTypeDef:
        """
        Modifies the number of days to retain snapshots in the destination Amazon Web
        Services Region after they are copied from the source Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_snapshot_copy_retention_period)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_snapshot_copy_retention_period)
        """

    async def modify_snapshot_schedule(
        self, *, ScheduleIdentifier: str, ScheduleDefinitions: Sequence[str]
    ) -> SnapshotScheduleResponseTypeDef:
        """
        Modifies a snapshot schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_snapshot_schedule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_snapshot_schedule)
        """

    async def modify_usage_limit(
        self,
        *,
        UsageLimitId: str,
        Amount: int = ...,
        BreachAction: UsageLimitBreachActionType = ...,
    ) -> UsageLimitResponseTypeDef:
        """
        Modifies a usage limit in a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.modify_usage_limit)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#modify_usage_limit)
        """

    async def pause_cluster(self, *, ClusterIdentifier: str) -> PauseClusterResultTypeDef:
        """
        Pauses a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.pause_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#pause_cluster)
        """

    async def purchase_reserved_node_offering(
        self, *, ReservedNodeOfferingId: str, NodeCount: int = ...
    ) -> PurchaseReservedNodeOfferingResultTypeDef:
        """
        Allows you to purchase reserved nodes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.purchase_reserved_node_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#purchase_reserved_node_offering)
        """

    async def put_resource_policy(
        self, *, ResourceArn: str, Policy: str
    ) -> PutResourcePolicyResultTypeDef:
        """
        Updates the resource policy for a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.put_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#put_resource_policy)
        """

    async def reboot_cluster(self, *, ClusterIdentifier: str) -> RebootClusterResultTypeDef:
        """
        Reboots a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.reboot_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#reboot_cluster)
        """

    async def reject_data_share(self, *, DataShareArn: str) -> DataShareResponseTypeDef:
        """
        From a datashare consumer account, rejects the specified datashare.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.reject_data_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#reject_data_share)
        """

    async def reset_cluster_parameter_group(
        self,
        *,
        ParameterGroupName: str,
        ResetAllParameters: bool = ...,
        Parameters: Sequence[ParameterTypeDef] = ...,
    ) -> ClusterParameterGroupNameMessageTypeDef:
        """
        Sets one or more parameters of the specified parameter group to their default
        values and sets the source values of the parameters to
        "engine-default".

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.reset_cluster_parameter_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#reset_cluster_parameter_group)
        """

    async def resize_cluster(
        self,
        *,
        ClusterIdentifier: str,
        ClusterType: str = ...,
        NodeType: str = ...,
        NumberOfNodes: int = ...,
        Classic: bool = ...,
        ReservedNodeId: str = ...,
        TargetReservedNodeOfferingId: str = ...,
    ) -> ResizeClusterResultTypeDef:
        """
        Changes the size of the cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.resize_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#resize_cluster)
        """

    async def restore_from_cluster_snapshot(
        self,
        *,
        ClusterIdentifier: str,
        SnapshotIdentifier: str = ...,
        SnapshotArn: str = ...,
        SnapshotClusterIdentifier: str = ...,
        Port: int = ...,
        AvailabilityZone: str = ...,
        AllowVersionUpgrade: bool = ...,
        ClusterSubnetGroupName: str = ...,
        PubliclyAccessible: bool = ...,
        OwnerAccount: str = ...,
        HsmClientCertificateIdentifier: str = ...,
        HsmConfigurationIdentifier: str = ...,
        ElasticIp: str = ...,
        ClusterParameterGroupName: str = ...,
        ClusterSecurityGroups: Sequence[str] = ...,
        VpcSecurityGroupIds: Sequence[str] = ...,
        PreferredMaintenanceWindow: str = ...,
        AutomatedSnapshotRetentionPeriod: int = ...,
        ManualSnapshotRetentionPeriod: int = ...,
        KmsKeyId: str = ...,
        NodeType: str = ...,
        EnhancedVpcRouting: bool = ...,
        AdditionalInfo: str = ...,
        IamRoles: Sequence[str] = ...,
        MaintenanceTrackName: str = ...,
        SnapshotScheduleIdentifier: str = ...,
        NumberOfNodes: int = ...,
        AvailabilityZoneRelocation: bool = ...,
        AquaConfigurationStatus: AquaConfigurationStatusType = ...,
        DefaultIamRoleArn: str = ...,
        ReservedNodeId: str = ...,
        TargetReservedNodeOfferingId: str = ...,
        Encrypted: bool = ...,
        ManageMasterPassword: bool = ...,
        MasterPasswordSecretKmsKeyId: str = ...,
        IpAddressType: str = ...,
        MultiAZ: bool = ...,
    ) -> RestoreFromClusterSnapshotResultTypeDef:
        """
        Creates a new cluster from a snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.restore_from_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#restore_from_cluster_snapshot)
        """

    async def restore_table_from_cluster_snapshot(
        self,
        *,
        ClusterIdentifier: str,
        SnapshotIdentifier: str,
        SourceDatabaseName: str,
        SourceTableName: str,
        NewTableName: str,
        SourceSchemaName: str = ...,
        TargetDatabaseName: str = ...,
        TargetSchemaName: str = ...,
        EnableCaseSensitiveIdentifier: bool = ...,
    ) -> RestoreTableFromClusterSnapshotResultTypeDef:
        """
        Creates a new table from a table in an Amazon Redshift cluster snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.restore_table_from_cluster_snapshot)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#restore_table_from_cluster_snapshot)
        """

    async def resume_cluster(self, *, ClusterIdentifier: str) -> ResumeClusterResultTypeDef:
        """
        Resumes a paused cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.resume_cluster)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#resume_cluster)
        """

    async def revoke_cluster_security_group_ingress(
        self,
        *,
        ClusterSecurityGroupName: str,
        CIDRIP: str = ...,
        EC2SecurityGroupName: str = ...,
        EC2SecurityGroupOwnerId: str = ...,
    ) -> RevokeClusterSecurityGroupIngressResultTypeDef:
        """
        Revokes an ingress rule in an Amazon Redshift security group for a previously
        authorized IP range or Amazon EC2 security
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.revoke_cluster_security_group_ingress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#revoke_cluster_security_group_ingress)
        """

    async def revoke_endpoint_access(
        self,
        *,
        ClusterIdentifier: str = ...,
        Account: str = ...,
        VpcIds: Sequence[str] = ...,
        Force: bool = ...,
    ) -> EndpointAuthorizationResponseTypeDef:
        """
        Revokes access to a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.revoke_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#revoke_endpoint_access)
        """

    async def revoke_snapshot_access(
        self,
        *,
        AccountWithRestoreAccess: str,
        SnapshotIdentifier: str = ...,
        SnapshotArn: str = ...,
        SnapshotClusterIdentifier: str = ...,
    ) -> RevokeSnapshotAccessResultTypeDef:
        """
        Removes the ability of the specified Amazon Web Services account to restore the
        specified
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.revoke_snapshot_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#revoke_snapshot_access)
        """

    async def rotate_encryption_key(
        self, *, ClusterIdentifier: str
    ) -> RotateEncryptionKeyResultTypeDef:
        """
        Rotates the encryption keys for a cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.rotate_encryption_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#rotate_encryption_key)
        """

    async def update_partner_status(
        self,
        *,
        AccountId: str,
        ClusterIdentifier: str,
        DatabaseName: str,
        PartnerName: str,
        Status: PartnerIntegrationStatusType,
        StatusMessage: str = ...,
    ) -> PartnerIntegrationOutputMessageTypeDef:
        """
        Updates the status of a partner integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.update_partner_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#update_partner_status)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_db_revisions"]
    ) -> DescribeClusterDbRevisionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_parameter_groups"]
    ) -> DescribeClusterParameterGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_parameters"]
    ) -> DescribeClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_security_groups"]
    ) -> DescribeClusterSecurityGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_snapshots"]
    ) -> DescribeClusterSnapshotsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_subnet_groups"]
    ) -> DescribeClusterSubnetGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_tracks"]
    ) -> DescribeClusterTracksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_cluster_versions"]
    ) -> DescribeClusterVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_clusters"]
    ) -> DescribeClustersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_custom_domain_associations"]
    ) -> DescribeCustomDomainAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares"]
    ) -> DescribeDataSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares_for_consumer"]
    ) -> DescribeDataSharesForConsumerPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_data_shares_for_producer"]
    ) -> DescribeDataSharesForProducerPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_default_cluster_parameters"]
    ) -> DescribeDefaultClusterParametersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_access"]
    ) -> DescribeEndpointAccessPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_endpoint_authorization"]
    ) -> DescribeEndpointAuthorizationPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_event_subscriptions"]
    ) -> DescribeEventSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_events"]) -> DescribeEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_hsm_client_certificates"]
    ) -> DescribeHsmClientCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_hsm_configurations"]
    ) -> DescribeHsmConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_inbound_integrations"]
    ) -> DescribeInboundIntegrationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_node_configuration_options"]
    ) -> DescribeNodeConfigurationOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_orderable_cluster_options"]
    ) -> DescribeOrderableClusterOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_redshift_idc_applications"]
    ) -> DescribeRedshiftIdcApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_node_exchange_status"]
    ) -> DescribeReservedNodeExchangeStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_node_offerings"]
    ) -> DescribeReservedNodeOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_reserved_nodes"]
    ) -> DescribeReservedNodesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scheduled_actions"]
    ) -> DescribeScheduledActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshot_copy_grants"]
    ) -> DescribeSnapshotCopyGrantsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_snapshot_schedules"]
    ) -> DescribeSnapshotSchedulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_table_restore_status"]
    ) -> DescribeTableRestoreStatusPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_tags"]) -> DescribeTagsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_usage_limits"]
    ) -> DescribeUsageLimitsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_reserved_node_exchange_configuration_options"]
    ) -> GetReservedNodeExchangeConfigurationOptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_reserved_node_exchange_offerings"]
    ) -> GetReservedNodeExchangeOfferingsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recommendations"]
    ) -> ListRecommendationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_available"]) -> ClusterAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_deleted"]) -> ClusterDeletedWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["cluster_restored"]) -> ClusterRestoredWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["snapshot_available"]) -> SnapshotAvailableWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/#get_waiter)
        """

    async def __aenter__(self) -> "RedshiftClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift/client/)
        """
