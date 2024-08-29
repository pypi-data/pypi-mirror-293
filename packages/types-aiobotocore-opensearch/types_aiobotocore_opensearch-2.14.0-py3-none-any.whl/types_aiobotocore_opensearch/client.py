"""
Type annotations for opensearch service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_opensearch.client import OpenSearchServiceClient

    session = get_session()
    async with session.create_client("opensearch") as client:
        client: OpenSearchServiceClient
    ```
"""

from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionTypeType,
    ConnectionModeType,
    DataSourceStatusType,
    DryRunModeType,
    EngineTypeType,
    IPAddressTypeType,
    LogTypeType,
    MaintenanceStatusType,
    MaintenanceTypeType,
    OpenSearchPartitionInstanceTypeType,
    PackageTypeType,
    ScheduleAtType,
)
from .type_defs import (
    AcceptInboundConnectionResponseTypeDef,
    AddDataSourceResponseTypeDef,
    AdvancedSecurityOptionsInputTypeDef,
    AIMLOptionsInputTypeDef,
    AssociatePackageResponseTypeDef,
    AuthorizeVpcEndpointAccessResponseTypeDef,
    AutoTuneOptionsInputTypeDef,
    AutoTuneOptionsUnionTypeDef,
    CancelDomainConfigChangeResponseTypeDef,
    CancelServiceSoftwareUpdateResponseTypeDef,
    ClusterConfigTypeDef,
    CognitoOptionsTypeDef,
    ConnectionPropertiesTypeDef,
    CreateDomainResponseTypeDef,
    CreateOutboundConnectionResponseTypeDef,
    CreatePackageResponseTypeDef,
    CreateVpcEndpointResponseTypeDef,
    DataSourceTypeTypeDef,
    DeleteDataSourceResponseTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteInboundConnectionResponseTypeDef,
    DeleteOutboundConnectionResponseTypeDef,
    DeletePackageResponseTypeDef,
    DeleteVpcEndpointResponseTypeDef,
    DescribeDomainAutoTunesResponseTypeDef,
    DescribeDomainChangeProgressResponseTypeDef,
    DescribeDomainConfigResponseTypeDef,
    DescribeDomainHealthResponseTypeDef,
    DescribeDomainNodesResponseTypeDef,
    DescribeDomainResponseTypeDef,
    DescribeDomainsResponseTypeDef,
    DescribeDryRunProgressResponseTypeDef,
    DescribeInboundConnectionsResponseTypeDef,
    DescribeInstanceTypeLimitsResponseTypeDef,
    DescribeOutboundConnectionsResponseTypeDef,
    DescribePackagesFilterTypeDef,
    DescribePackagesResponseTypeDef,
    DescribeReservedInstanceOfferingsResponseTypeDef,
    DescribeReservedInstancesResponseTypeDef,
    DescribeVpcEndpointsResponseTypeDef,
    DissociatePackageResponseTypeDef,
    DomainEndpointOptionsTypeDef,
    DomainInformationContainerTypeDef,
    EBSOptionsTypeDef,
    EmptyResponseMetadataTypeDef,
    EncryptionAtRestOptionsTypeDef,
    FilterTypeDef,
    GetCompatibleVersionsResponseTypeDef,
    GetDataSourceResponseTypeDef,
    GetDomainMaintenanceStatusResponseTypeDef,
    GetPackageVersionHistoryResponseTypeDef,
    GetUpgradeHistoryResponseTypeDef,
    GetUpgradeStatusResponseTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDomainMaintenancesResponseTypeDef,
    ListDomainNamesResponseTypeDef,
    ListDomainsForPackageResponseTypeDef,
    ListInstanceTypeDetailsResponseTypeDef,
    ListPackagesForDomainResponseTypeDef,
    ListScheduledActionsResponseTypeDef,
    ListTagsResponseTypeDef,
    ListVersionsResponseTypeDef,
    ListVpcEndpointAccessResponseTypeDef,
    ListVpcEndpointsForDomainResponseTypeDef,
    ListVpcEndpointsResponseTypeDef,
    LogPublishingOptionTypeDef,
    NodeToNodeEncryptionOptionsTypeDef,
    OffPeakWindowOptionsTypeDef,
    PackageSourceTypeDef,
    PurchaseReservedInstanceOfferingResponseTypeDef,
    RejectInboundConnectionResponseTypeDef,
    SnapshotOptionsTypeDef,
    SoftwareUpdateOptionsTypeDef,
    StartDomainMaintenanceResponseTypeDef,
    StartServiceSoftwareUpdateResponseTypeDef,
    TagTypeDef,
    UpdateDataSourceResponseTypeDef,
    UpdateDomainConfigResponseTypeDef,
    UpdatePackageResponseTypeDef,
    UpdateScheduledActionResponseTypeDef,
    UpdateVpcEndpointResponseTypeDef,
    UpgradeDomainResponseTypeDef,
    VPCOptionsTypeDef,
)

__all__ = ("OpenSearchServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BaseException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailureException: Type[BotocoreClientError]
    DisabledOperationException: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidPaginationTokenException: Type[BotocoreClientError]
    InvalidTypeException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    SlotNotAvailableException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class OpenSearchServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        OpenSearchServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#exceptions)
        """

    async def accept_inbound_connection(
        self, *, ConnectionId: str
    ) -> AcceptInboundConnectionResponseTypeDef:
        """
        Allows the destination Amazon OpenSearch Service domain owner to accept an
        inbound cross-cluster search connection
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.accept_inbound_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#accept_inbound_connection)
        """

    async def add_data_source(
        self,
        *,
        DomainName: str,
        Name: str,
        DataSourceType: DataSourceTypeTypeDef,
        Description: str = ...,
    ) -> AddDataSourceResponseTypeDef:
        """
        Creates a new direct-query data source to the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.add_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#add_data_source)
        """

    async def add_tags(
        self, *, ARN: str, TagList: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches tags to an existing Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.add_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#add_tags)
        """

    async def associate_package(
        self, *, PackageID: str, DomainName: str
    ) -> AssociatePackageResponseTypeDef:
        """
        Associates a package with an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.associate_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#associate_package)
        """

    async def authorize_vpc_endpoint_access(
        self, *, DomainName: str, Account: str
    ) -> AuthorizeVpcEndpointAccessResponseTypeDef:
        """
        Provides access to an Amazon OpenSearch Service domain through the use of an
        interface VPC
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.authorize_vpc_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#authorize_vpc_endpoint_access)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#can_paginate)
        """

    async def cancel_domain_config_change(
        self, *, DomainName: str, DryRun: bool = ...
    ) -> CancelDomainConfigChangeResponseTypeDef:
        """
        Cancels a pending configuration change on an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.cancel_domain_config_change)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#cancel_domain_config_change)
        """

    async def cancel_service_software_update(
        self, *, DomainName: str
    ) -> CancelServiceSoftwareUpdateResponseTypeDef:
        """
        Cancels a scheduled service software update for an Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.cancel_service_software_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#cancel_service_software_update)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#close)
        """

    async def create_domain(
        self,
        *,
        DomainName: str,
        EngineVersion: str = ...,
        ClusterConfig: ClusterConfigTypeDef = ...,
        EBSOptions: EBSOptionsTypeDef = ...,
        AccessPolicies: str = ...,
        IPAddressType: IPAddressTypeType = ...,
        SnapshotOptions: SnapshotOptionsTypeDef = ...,
        VPCOptions: VPCOptionsTypeDef = ...,
        CognitoOptions: CognitoOptionsTypeDef = ...,
        EncryptionAtRestOptions: EncryptionAtRestOptionsTypeDef = ...,
        NodeToNodeEncryptionOptions: NodeToNodeEncryptionOptionsTypeDef = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        LogPublishingOptions: Mapping[LogTypeType, LogPublishingOptionTypeDef] = ...,
        DomainEndpointOptions: DomainEndpointOptionsTypeDef = ...,
        AdvancedSecurityOptions: AdvancedSecurityOptionsInputTypeDef = ...,
        TagList: Sequence[TagTypeDef] = ...,
        AutoTuneOptions: AutoTuneOptionsInputTypeDef = ...,
        OffPeakWindowOptions: OffPeakWindowOptionsTypeDef = ...,
        SoftwareUpdateOptions: SoftwareUpdateOptionsTypeDef = ...,
        AIMLOptions: AIMLOptionsInputTypeDef = ...,
    ) -> CreateDomainResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.create_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_domain)
        """

    async def create_outbound_connection(
        self,
        *,
        LocalDomainInfo: DomainInformationContainerTypeDef,
        RemoteDomainInfo: DomainInformationContainerTypeDef,
        ConnectionAlias: str,
        ConnectionMode: ConnectionModeType = ...,
        ConnectionProperties: ConnectionPropertiesTypeDef = ...,
    ) -> CreateOutboundConnectionResponseTypeDef:
        """
        Creates a new cross-cluster search connection from a source Amazon OpenSearch
        Service domain to a destination
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.create_outbound_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_outbound_connection)
        """

    async def create_package(
        self,
        *,
        PackageName: str,
        PackageType: PackageTypeType,
        PackageSource: PackageSourceTypeDef,
        PackageDescription: str = ...,
    ) -> CreatePackageResponseTypeDef:
        """
        Creates a package for use with Amazon OpenSearch Service domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.create_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_package)
        """

    async def create_vpc_endpoint(
        self, *, DomainArn: str, VpcOptions: VPCOptionsTypeDef, ClientToken: str = ...
    ) -> CreateVpcEndpointResponseTypeDef:
        """
        Creates an Amazon OpenSearch Service-managed VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.create_vpc_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#create_vpc_endpoint)
        """

    async def delete_data_source(
        self, *, DomainName: str, Name: str
    ) -> DeleteDataSourceResponseTypeDef:
        """
        Deletes a direct-query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_data_source)
        """

    async def delete_domain(self, *, DomainName: str) -> DeleteDomainResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service domain and all of its data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_domain)
        """

    async def delete_inbound_connection(
        self, *, ConnectionId: str
    ) -> DeleteInboundConnectionResponseTypeDef:
        """
        Allows the destination Amazon OpenSearch Service domain owner to delete an
        existing inbound cross-cluster search
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_inbound_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_inbound_connection)
        """

    async def delete_outbound_connection(
        self, *, ConnectionId: str
    ) -> DeleteOutboundConnectionResponseTypeDef:
        """
        Allows the source Amazon OpenSearch Service domain owner to delete an existing
        outbound cross-cluster search
        connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_outbound_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_outbound_connection)
        """

    async def delete_package(self, *, PackageID: str) -> DeletePackageResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_package)
        """

    async def delete_vpc_endpoint(self, *, VpcEndpointId: str) -> DeleteVpcEndpointResponseTypeDef:
        """
        Deletes an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.delete_vpc_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#delete_vpc_endpoint)
        """

    async def describe_domain(self, *, DomainName: str) -> DescribeDomainResponseTypeDef:
        """
        Describes the domain configuration for the specified Amazon OpenSearch Service
        domain, including the domain ID, domain service endpoint, and domain
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain)
        """

    async def describe_domain_auto_tunes(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeDomainAutoTunesResponseTypeDef:
        """
        Returns the list of optimizations that Auto-Tune has made to an Amazon
        OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain_auto_tunes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_auto_tunes)
        """

    async def describe_domain_change_progress(
        self, *, DomainName: str, ChangeId: str = ...
    ) -> DescribeDomainChangeProgressResponseTypeDef:
        """
        Returns information about the current blue/green deployment happening on an
        Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain_change_progress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_change_progress)
        """

    async def describe_domain_config(
        self, *, DomainName: str
    ) -> DescribeDomainConfigResponseTypeDef:
        """
        Returns the configuration of an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_config)
        """

    async def describe_domain_health(
        self, *, DomainName: str
    ) -> DescribeDomainHealthResponseTypeDef:
        """
        Returns information about domain and node health, the standby Availability
        Zone, number of nodes per Availability Zone, and shard count per
        node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain_health)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_health)
        """

    async def describe_domain_nodes(self, *, DomainName: str) -> DescribeDomainNodesResponseTypeDef:
        """
        Returns information about domain and nodes, including data nodes, master nodes,
        ultrawarm nodes, Availability Zone(s), standby nodes, node configurations, and
        node
        states.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domain_nodes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domain_nodes)
        """

    async def describe_domains(
        self, *, DomainNames: Sequence[str]
    ) -> DescribeDomainsResponseTypeDef:
        """
        Returns domain configuration information about the specified Amazon OpenSearch
        Service
        domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_domains)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_domains)
        """

    async def describe_dry_run_progress(
        self, *, DomainName: str, DryRunId: str = ..., LoadDryRunConfig: bool = ...
    ) -> DescribeDryRunProgressResponseTypeDef:
        """
        Describes the progress of a pre-update dry run analysis on an Amazon OpenSearch
        Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_dry_run_progress)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_dry_run_progress)
        """

    async def describe_inbound_connections(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeInboundConnectionsResponseTypeDef:
        """
        Lists all the inbound cross-cluster search connections for a destination
        (remote) Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_inbound_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_inbound_connections)
        """

    async def describe_instance_type_limits(
        self,
        *,
        InstanceType: OpenSearchPartitionInstanceTypeType,
        EngineVersion: str,
        DomainName: str = ...,
    ) -> DescribeInstanceTypeLimitsResponseTypeDef:
        """
        Describes the instance count, storage, and master node limits for a given
        OpenSearch or Elasticsearch version and instance
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_instance_type_limits)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_instance_type_limits)
        """

    async def describe_outbound_connections(
        self, *, Filters: Sequence[FilterTypeDef] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeOutboundConnectionsResponseTypeDef:
        """
        Lists all the outbound cross-cluster connections for a local (source) Amazon
        OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_outbound_connections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_outbound_connections)
        """

    async def describe_packages(
        self,
        *,
        Filters: Sequence[DescribePackagesFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribePackagesResponseTypeDef:
        """
        Describes all packages available to OpenSearch Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_packages)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_packages)
        """

    async def describe_reserved_instance_offerings(
        self, *, ReservedInstanceOfferingId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeReservedInstanceOfferingsResponseTypeDef:
        """
        Describes the available Amazon OpenSearch Service Reserved Instance offerings
        for a given
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_reserved_instance_offerings)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_reserved_instance_offerings)
        """

    async def describe_reserved_instances(
        self, *, ReservedInstanceId: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeReservedInstancesResponseTypeDef:
        """
        Describes the Amazon OpenSearch Service instances that you have reserved in a
        given
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_reserved_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_reserved_instances)
        """

    async def describe_vpc_endpoints(
        self, *, VpcEndpointIds: Sequence[str]
    ) -> DescribeVpcEndpointsResponseTypeDef:
        """
        Describes one or more Amazon OpenSearch Service-managed VPC endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.describe_vpc_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#describe_vpc_endpoints)
        """

    async def dissociate_package(
        self, *, PackageID: str, DomainName: str
    ) -> DissociatePackageResponseTypeDef:
        """
        Removes a package from the specified Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.dissociate_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#dissociate_package)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#generate_presigned_url)
        """

    async def get_compatible_versions(
        self, *, DomainName: str = ...
    ) -> GetCompatibleVersionsResponseTypeDef:
        """
        Returns a map of OpenSearch or Elasticsearch versions and the versions you can
        upgrade them
        to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_compatible_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_compatible_versions)
        """

    async def get_data_source(self, *, DomainName: str, Name: str) -> GetDataSourceResponseTypeDef:
        """
        Retrieves information about a direct query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_data_source)
        """

    async def get_domain_maintenance_status(
        self, *, DomainName: str, MaintenanceId: str
    ) -> GetDomainMaintenanceStatusResponseTypeDef:
        """
        The status of the maintenance action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_domain_maintenance_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_domain_maintenance_status)
        """

    async def get_package_version_history(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetPackageVersionHistoryResponseTypeDef:
        """
        Returns a list of Amazon OpenSearch Service package versions, along with their
        creation time, commit message, and plugin properties (if the package is a zip
        plugin
        package).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_package_version_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_package_version_history)
        """

    async def get_upgrade_history(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> GetUpgradeHistoryResponseTypeDef:
        """
        Retrieves the complete history of the last 10 upgrades performed on an Amazon
        OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_upgrade_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_upgrade_history)
        """

    async def get_upgrade_status(self, *, DomainName: str) -> GetUpgradeStatusResponseTypeDef:
        """
        Returns the most recent status of the last upgrade or upgrade eligibility check
        performed on an Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.get_upgrade_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#get_upgrade_status)
        """

    async def list_data_sources(self, *, DomainName: str) -> ListDataSourcesResponseTypeDef:
        """
        Lists direct-query data sources for a specific domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_data_sources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_data_sources)
        """

    async def list_domain_maintenances(
        self,
        *,
        DomainName: str,
        Action: MaintenanceTypeType = ...,
        Status: MaintenanceStatusType = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListDomainMaintenancesResponseTypeDef:
        """
        A list of maintenance actions for the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_domain_maintenances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domain_maintenances)
        """

    async def list_domain_names(
        self, *, EngineType: EngineTypeType = ...
    ) -> ListDomainNamesResponseTypeDef:
        """
        Returns the names of all Amazon OpenSearch Service domains owned by the current
        user in the active
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_domain_names)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domain_names)
        """

    async def list_domains_for_package(
        self, *, PackageID: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListDomainsForPackageResponseTypeDef:
        """
        Lists all Amazon OpenSearch Service domains associated with a given package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_domains_for_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_domains_for_package)
        """

    async def list_instance_type_details(
        self,
        *,
        EngineVersion: str,
        DomainName: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        RetrieveAZs: bool = ...,
        InstanceType: str = ...,
    ) -> ListInstanceTypeDetailsResponseTypeDef:
        """
        Lists all instance types and available features for a given OpenSearch or
        Elasticsearch
        version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_instance_type_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_instance_type_details)
        """

    async def list_packages_for_domain(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPackagesForDomainResponseTypeDef:
        """
        Lists all packages associated with an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_packages_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_packages_for_domain)
        """

    async def list_scheduled_actions(
        self, *, DomainName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListScheduledActionsResponseTypeDef:
        """
        Retrieves a list of configuration changes that are scheduled for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_scheduled_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_scheduled_actions)
        """

    async def list_tags(self, *, ARN: str) -> ListTagsResponseTypeDef:
        """
        Returns all resource tags for an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_tags)
        """

    async def list_versions(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListVersionsResponseTypeDef:
        """
        Lists all versions of OpenSearch and Elasticsearch that Amazon OpenSearch
        Service
        supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_versions)
        """

    async def list_vpc_endpoint_access(
        self, *, DomainName: str, NextToken: str = ...
    ) -> ListVpcEndpointAccessResponseTypeDef:
        """
        Retrieves information about each Amazon Web Services principal that is allowed
        to access a given Amazon OpenSearch Service domain through the use of an
        interface VPC
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_vpc_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoint_access)
        """

    async def list_vpc_endpoints(self, *, NextToken: str = ...) -> ListVpcEndpointsResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints in the current
        Amazon Web Services account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_vpc_endpoints)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoints)
        """

    async def list_vpc_endpoints_for_domain(
        self, *, DomainName: str, NextToken: str = ...
    ) -> ListVpcEndpointsForDomainResponseTypeDef:
        """
        Retrieves all Amazon OpenSearch Service-managed VPC endpoints associated with a
        particular
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.list_vpc_endpoints_for_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#list_vpc_endpoints_for_domain)
        """

    async def purchase_reserved_instance_offering(
        self, *, ReservedInstanceOfferingId: str, ReservationName: str, InstanceCount: int = ...
    ) -> PurchaseReservedInstanceOfferingResponseTypeDef:
        """
        Allows you to purchase Amazon OpenSearch Service Reserved Instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.purchase_reserved_instance_offering)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#purchase_reserved_instance_offering)
        """

    async def reject_inbound_connection(
        self, *, ConnectionId: str
    ) -> RejectInboundConnectionResponseTypeDef:
        """
        Allows the remote Amazon OpenSearch Service domain owner to reject an inbound
        cross-cluster connection
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.reject_inbound_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#reject_inbound_connection)
        """

    async def remove_tags(
        self, *, ARN: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified set of tags from an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.remove_tags)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#remove_tags)
        """

    async def revoke_vpc_endpoint_access(self, *, DomainName: str, Account: str) -> Dict[str, Any]:
        """
        Revokes access to an Amazon OpenSearch Service domain that was provided through
        an interface VPC
        endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.revoke_vpc_endpoint_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#revoke_vpc_endpoint_access)
        """

    async def start_domain_maintenance(
        self, *, DomainName: str, Action: MaintenanceTypeType, NodeId: str = ...
    ) -> StartDomainMaintenanceResponseTypeDef:
        """
        Starts the node maintenance process on the data node.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.start_domain_maintenance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#start_domain_maintenance)
        """

    async def start_service_software_update(
        self, *, DomainName: str, ScheduleAt: ScheduleAtType = ..., DesiredStartTime: int = ...
    ) -> StartServiceSoftwareUpdateResponseTypeDef:
        """
        Schedules a service software update for an Amazon OpenSearch Service domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.start_service_software_update)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#start_service_software_update)
        """

    async def update_data_source(
        self,
        *,
        DomainName: str,
        Name: str,
        DataSourceType: DataSourceTypeTypeDef,
        Description: str = ...,
        Status: DataSourceStatusType = ...,
    ) -> UpdateDataSourceResponseTypeDef:
        """
        Updates a direct-query data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.update_data_source)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_data_source)
        """

    async def update_domain_config(
        self,
        *,
        DomainName: str,
        ClusterConfig: ClusterConfigTypeDef = ...,
        EBSOptions: EBSOptionsTypeDef = ...,
        SnapshotOptions: SnapshotOptionsTypeDef = ...,
        VPCOptions: VPCOptionsTypeDef = ...,
        CognitoOptions: CognitoOptionsTypeDef = ...,
        AdvancedOptions: Mapping[str, str] = ...,
        AccessPolicies: str = ...,
        IPAddressType: IPAddressTypeType = ...,
        LogPublishingOptions: Mapping[LogTypeType, LogPublishingOptionTypeDef] = ...,
        EncryptionAtRestOptions: EncryptionAtRestOptionsTypeDef = ...,
        DomainEndpointOptions: DomainEndpointOptionsTypeDef = ...,
        NodeToNodeEncryptionOptions: NodeToNodeEncryptionOptionsTypeDef = ...,
        AdvancedSecurityOptions: AdvancedSecurityOptionsInputTypeDef = ...,
        AutoTuneOptions: AutoTuneOptionsUnionTypeDef = ...,
        DryRun: bool = ...,
        DryRunMode: DryRunModeType = ...,
        OffPeakWindowOptions: OffPeakWindowOptionsTypeDef = ...,
        SoftwareUpdateOptions: SoftwareUpdateOptionsTypeDef = ...,
        AIMLOptions: AIMLOptionsInputTypeDef = ...,
    ) -> UpdateDomainConfigResponseTypeDef:
        """
        Modifies the cluster configuration of the specified Amazon OpenSearch Service
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.update_domain_config)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_domain_config)
        """

    async def update_package(
        self,
        *,
        PackageID: str,
        PackageSource: PackageSourceTypeDef,
        PackageDescription: str = ...,
        CommitMessage: str = ...,
    ) -> UpdatePackageResponseTypeDef:
        """
        Updates a package for use with Amazon OpenSearch Service domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.update_package)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_package)
        """

    async def update_scheduled_action(
        self,
        *,
        DomainName: str,
        ActionID: str,
        ActionType: ActionTypeType,
        ScheduleAt: ScheduleAtType,
        DesiredStartTime: int = ...,
    ) -> UpdateScheduledActionResponseTypeDef:
        """
        Reschedules a planned domain configuration change for a later time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.update_scheduled_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_scheduled_action)
        """

    async def update_vpc_endpoint(
        self, *, VpcEndpointId: str, VpcOptions: VPCOptionsTypeDef
    ) -> UpdateVpcEndpointResponseTypeDef:
        """
        Modifies an Amazon OpenSearch Service-managed interface VPC endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.update_vpc_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#update_vpc_endpoint)
        """

    async def upgrade_domain(
        self,
        *,
        DomainName: str,
        TargetVersion: str,
        PerformCheckOnly: bool = ...,
        AdvancedOptions: Mapping[str, str] = ...,
    ) -> UpgradeDomainResponseTypeDef:
        """
        Allows you to either upgrade your Amazon OpenSearch Service domain or perform
        an upgrade eligibility check to a compatible version of OpenSearch or
        Elasticsearch.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client.upgrade_domain)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/#upgrade_domain)
        """

    async def __aenter__(self) -> "OpenSearchServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/opensearch.html#OpenSearchService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_opensearch/client/)
        """
