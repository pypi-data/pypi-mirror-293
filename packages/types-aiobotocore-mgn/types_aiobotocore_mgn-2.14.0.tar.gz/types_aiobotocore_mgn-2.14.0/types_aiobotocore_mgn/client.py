"""
Type annotations for mgn service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mgn.client import MgnClient

    session = get_session()
    async with session.create_client("mgn") as client:
        client: MgnClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ActionCategoryType,
    BootModeType,
    LaunchDispositionType,
    ReplicationConfigurationDataPlaneRoutingType,
    ReplicationConfigurationDefaultLargeStagingDiskTypeType,
    ReplicationConfigurationEbsEncryptionType,
    ReplicationTypeType,
    TargetInstanceTypeRightSizingMethodType,
)
from .paginator import (
    DescribeJobLogItemsPaginator,
    DescribeJobsPaginator,
    DescribeLaunchConfigurationTemplatesPaginator,
    DescribeReplicationConfigurationTemplatesPaginator,
    DescribeSourceServersPaginator,
    DescribeVcenterClientsPaginator,
    ListApplicationsPaginator,
    ListConnectorsPaginator,
    ListExportErrorsPaginator,
    ListExportsPaginator,
    ListImportErrorsPaginator,
    ListImportsPaginator,
    ListManagedAccountsPaginator,
    ListSourceServerActionsPaginator,
    ListTemplateActionsPaginator,
    ListWavesPaginator,
)
from .type_defs import (
    ApplicationResponseTypeDef,
    ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
    ConnectorResponseTypeDef,
    ConnectorSsmCommandConfigTypeDef,
    DescribeJobLogItemsResponseTypeDef,
    DescribeJobsRequestFiltersTypeDef,
    DescribeJobsResponseTypeDef,
    DescribeLaunchConfigurationTemplatesResponseTypeDef,
    DescribeReplicationConfigurationTemplatesResponseTypeDef,
    DescribeSourceServersRequestFiltersTypeDef,
    DescribeSourceServersResponseTypeDef,
    DescribeVcenterClientsResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    LaunchConfigurationTemplateResponseTypeDef,
    LaunchConfigurationTypeDef,
    LaunchTemplateDiskConfTypeDef,
    LicensingTypeDef,
    ListApplicationsRequestFiltersTypeDef,
    ListApplicationsResponseTypeDef,
    ListConnectorsRequestFiltersTypeDef,
    ListConnectorsResponseTypeDef,
    ListExportErrorsResponseTypeDef,
    ListExportsRequestFiltersTypeDef,
    ListExportsResponseTypeDef,
    ListImportErrorsResponseTypeDef,
    ListImportsRequestFiltersTypeDef,
    ListImportsResponseTypeDef,
    ListManagedAccountsResponseTypeDef,
    ListSourceServerActionsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTemplateActionsResponseTypeDef,
    ListWavesRequestFiltersTypeDef,
    ListWavesResponseTypeDef,
    PostLaunchActionsUnionTypeDef,
    ReplicationConfigurationReplicatedDiskTypeDef,
    ReplicationConfigurationTemplateResponseTypeDef,
    ReplicationConfigurationTypeDef,
    S3BucketSourceTypeDef,
    SourceServerActionDocumentResponseTypeDef,
    SourceServerActionsRequestFiltersTypeDef,
    SourceServerConnectorActionTypeDef,
    SourceServerResponseTypeDef,
    SsmExternalParameterTypeDef,
    SsmParameterStoreParameterTypeDef,
    StartCutoverResponseTypeDef,
    StartExportResponseTypeDef,
    StartImportResponseTypeDef,
    StartTestResponseTypeDef,
    TemplateActionDocumentResponseTypeDef,
    TemplateActionsRequestFiltersTypeDef,
    TerminateTargetInstancesResponseTypeDef,
    WaveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("MgnClient",)


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
    UninitializedAccountException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MgnClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MgnClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#exceptions)
        """

    async def archive_application(
        self, *, applicationID: str, accountID: str = ...
    ) -> ApplicationResponseTypeDef:
        """
        Archive application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.archive_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#archive_application)
        """

    async def archive_wave(self, *, waveID: str, accountID: str = ...) -> WaveResponseTypeDef:
        """
        Archive wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.archive_wave)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#archive_wave)
        """

    async def associate_applications(
        self, *, applicationIDs: Sequence[str], waveID: str, accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Associate applications to wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.associate_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#associate_applications)
        """

    async def associate_source_servers(
        self, *, applicationID: str, sourceServerIDs: Sequence[str], accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Associate source servers to application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.associate_source_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#associate_source_servers)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#can_paginate)
        """

    async def change_server_life_cycle_state(
        self,
        *,
        lifeCycle: ChangeServerLifeCycleStateSourceServerLifecycleTypeDef,
        sourceServerID: str,
        accountID: str = ...,
    ) -> SourceServerResponseTypeDef:
        """
        Allows the user to set the SourceServer.LifeCycle.state property for specific
        Source Server IDs to one of the following: READY_FOR_TEST or
        READY_FOR_CUTOVER.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.change_server_life_cycle_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#change_server_life_cycle_state)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#close)
        """

    async def create_application(
        self,
        *,
        name: str,
        accountID: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> ApplicationResponseTypeDef:
        """
        Create application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.create_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#create_application)
        """

    async def create_connector(
        self,
        *,
        name: str,
        ssmInstanceID: str,
        ssmCommandConfig: ConnectorSsmCommandConfigTypeDef = ...,
        tags: Mapping[str, str] = ...,
    ) -> ConnectorResponseTypeDef:
        """
        Create Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.create_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#create_connector)
        """

    async def create_launch_configuration_template(
        self,
        *,
        associatePublicIpAddress: bool = ...,
        bootMode: BootModeType = ...,
        copyPrivateIp: bool = ...,
        copyTags: bool = ...,
        enableMapAutoTagging: bool = ...,
        largeVolumeConf: LaunchTemplateDiskConfTypeDef = ...,
        launchDisposition: LaunchDispositionType = ...,
        licensing: LicensingTypeDef = ...,
        mapAutoTaggingMpeID: str = ...,
        postLaunchActions: PostLaunchActionsUnionTypeDef = ...,
        smallVolumeConf: LaunchTemplateDiskConfTypeDef = ...,
        smallVolumeMaxSize: int = ...,
        tags: Mapping[str, str] = ...,
        targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType = ...,
    ) -> LaunchConfigurationTemplateResponseTypeDef:
        """
        Creates a new Launch Configuration Template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.create_launch_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#create_launch_configuration_template)
        """

    async def create_replication_configuration_template(
        self,
        *,
        associateDefaultSecurityGroup: bool,
        bandwidthThrottling: int,
        createPublicIP: bool,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType,
        replicationServerInstanceType: str,
        replicationServersSecurityGroupsIDs: Sequence[str],
        stagingAreaSubnetId: str,
        stagingAreaTags: Mapping[str, str],
        useDedicatedReplicationServer: bool,
        ebsEncryptionKeyArn: str = ...,
        tags: Mapping[str, str] = ...,
        useFipsEndpoint: bool = ...,
    ) -> ReplicationConfigurationTemplateResponseTypeDef:
        """
        Creates a new ReplicationConfigurationTemplate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.create_replication_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#create_replication_configuration_template)
        """

    async def create_wave(
        self,
        *,
        name: str,
        accountID: str = ...,
        description: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> WaveResponseTypeDef:
        """
        Create wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.create_wave)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#create_wave)
        """

    async def delete_application(
        self, *, applicationID: str, accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Delete application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_application)
        """

    async def delete_connector(self, *, connectorID: str) -> EmptyResponseMetadataTypeDef:
        """
        Delete Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_connector)
        """

    async def delete_job(self, *, jobID: str, accountID: str = ...) -> Dict[str, Any]:
        """
        Deletes a single Job by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_job)
        """

    async def delete_launch_configuration_template(
        self, *, launchConfigurationTemplateID: str
    ) -> Dict[str, Any]:
        """
        Deletes a single Launch Configuration Template by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_launch_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_launch_configuration_template)
        """

    async def delete_replication_configuration_template(
        self, *, replicationConfigurationTemplateID: str
    ) -> Dict[str, Any]:
        """
        Deletes a single Replication Configuration Template by ID See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mgn-2020-02-26/DeleteReplicationConfigurationTemplate).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_replication_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_replication_configuration_template)
        """

    async def delete_source_server(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Deletes a single source server by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_source_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_source_server)
        """

    async def delete_vcenter_client(self, *, vcenterClientID: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a given vCenter client by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_vcenter_client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_vcenter_client)
        """

    async def delete_wave(self, *, waveID: str, accountID: str = ...) -> Dict[str, Any]:
        """
        Delete wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.delete_wave)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#delete_wave)
        """

    async def describe_job_log_items(
        self, *, jobID: str, accountID: str = ..., maxResults: int = ..., nextToken: str = ...
    ) -> DescribeJobLogItemsResponseTypeDef:
        """
        Retrieves detailed job log items with paging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_job_log_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_job_log_items)
        """

    async def describe_jobs(
        self,
        *,
        accountID: str = ...,
        filters: DescribeJobsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> DescribeJobsResponseTypeDef:
        """
        Returns a list of Jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_jobs)
        """

    async def describe_launch_configuration_templates(
        self,
        *,
        launchConfigurationTemplateIDs: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> DescribeLaunchConfigurationTemplatesResponseTypeDef:
        """
        Lists all Launch Configuration Templates, filtered by Launch Configuration
        Template IDs See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/mgn-2020-02-26/DescribeLaunchConfigurationTemplates).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_launch_configuration_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_launch_configuration_templates)
        """

    async def describe_replication_configuration_templates(
        self,
        *,
        maxResults: int = ...,
        nextToken: str = ...,
        replicationConfigurationTemplateIDs: Sequence[str] = ...,
    ) -> DescribeReplicationConfigurationTemplatesResponseTypeDef:
        """
        Lists all ReplicationConfigurationTemplates, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_replication_configuration_templates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_replication_configuration_templates)
        """

    async def describe_source_servers(
        self,
        *,
        accountID: str = ...,
        filters: DescribeSourceServersRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> DescribeSourceServersResponseTypeDef:
        """
        Retrieves all SourceServers or multiple SourceServers by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_source_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_source_servers)
        """

    async def describe_vcenter_clients(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> DescribeVcenterClientsResponseTypeDef:
        """
        Returns a list of the installed vCenter clients.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.describe_vcenter_clients)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#describe_vcenter_clients)
        """

    async def disassociate_applications(
        self, *, applicationIDs: Sequence[str], waveID: str, accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociate applications from wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.disassociate_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#disassociate_applications)
        """

    async def disassociate_source_servers(
        self, *, applicationID: str, sourceServerIDs: Sequence[str], accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Disassociate source servers from application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.disassociate_source_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#disassociate_source_servers)
        """

    async def disconnect_from_service(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Disconnects specific Source Servers from Application Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.disconnect_from_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#disconnect_from_service)
        """

    async def finalize_cutover(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Finalizes the cutover immediately for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.finalize_cutover)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#finalize_cutover)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#generate_presigned_url)
        """

    async def get_launch_configuration(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> LaunchConfigurationTypeDef:
        """
        Lists all LaunchConfigurations available, filtered by Source Server IDs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_launch_configuration)
        """

    async def get_replication_configuration(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> ReplicationConfigurationTypeDef:
        """
        Lists all ReplicationConfigurations, filtered by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_replication_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_replication_configuration)
        """

    async def initialize_service(self) -> Dict[str, Any]:
        """
        Initialize Application Migration Service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.initialize_service)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#initialize_service)
        """

    async def list_applications(
        self,
        *,
        accountID: str = ...,
        filters: ListApplicationsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListApplicationsResponseTypeDef:
        """
        Retrieves all applications or multiple applications by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_applications)
        """

    async def list_connectors(
        self,
        *,
        filters: ListConnectorsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListConnectorsResponseTypeDef:
        """
        List Connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_connectors)
        """

    async def list_export_errors(
        self, *, exportID: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListExportErrorsResponseTypeDef:
        """
        List export errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_export_errors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_export_errors)
        """

    async def list_exports(
        self,
        *,
        filters: ListExportsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListExportsResponseTypeDef:
        """
        List exports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_exports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_exports)
        """

    async def list_import_errors(
        self, *, importID: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListImportErrorsResponseTypeDef:
        """
        List import errors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_import_errors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_import_errors)
        """

    async def list_imports(
        self,
        *,
        filters: ListImportsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListImportsResponseTypeDef:
        """
        List imports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_imports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_imports)
        """

    async def list_managed_accounts(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListManagedAccountsResponseTypeDef:
        """
        List Managed Accounts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_managed_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_managed_accounts)
        """

    async def list_source_server_actions(
        self,
        *,
        sourceServerID: str,
        accountID: str = ...,
        filters: SourceServerActionsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListSourceServerActionsResponseTypeDef:
        """
        List source server post migration custom actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_source_server_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_source_server_actions)
        """

    async def list_tags_for_resource(
        self, *, resourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags for your Application Migration Service resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_tags_for_resource)
        """

    async def list_template_actions(
        self,
        *,
        launchConfigurationTemplateID: str,
        filters: TemplateActionsRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListTemplateActionsResponseTypeDef:
        """
        List template post migration custom actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_template_actions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_template_actions)
        """

    async def list_waves(
        self,
        *,
        accountID: str = ...,
        filters: ListWavesRequestFiltersTypeDef = ...,
        maxResults: int = ...,
        nextToken: str = ...,
    ) -> ListWavesResponseTypeDef:
        """
        Retrieves all waves or multiple waves by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.list_waves)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#list_waves)
        """

    async def mark_as_archived(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Archives specific Source Servers by setting the SourceServer.isArchived
        property to true for specified SourceServers by
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.mark_as_archived)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#mark_as_archived)
        """

    async def pause_replication(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Pause Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.pause_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#pause_replication)
        """

    async def put_source_server_action(
        self,
        *,
        actionID: str,
        actionName: str,
        documentIdentifier: str,
        order: int,
        sourceServerID: str,
        accountID: str = ...,
        active: bool = ...,
        category: ActionCategoryType = ...,
        description: str = ...,
        documentVersion: str = ...,
        externalParameters: Mapping[str, SsmExternalParameterTypeDef] = ...,
        mustSucceedForCutover: bool = ...,
        parameters: Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]] = ...,
        timeoutSeconds: int = ...,
    ) -> SourceServerActionDocumentResponseTypeDef:
        """
        Put source server post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.put_source_server_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#put_source_server_action)
        """

    async def put_template_action(
        self,
        *,
        actionID: str,
        actionName: str,
        documentIdentifier: str,
        launchConfigurationTemplateID: str,
        order: int,
        active: bool = ...,
        category: ActionCategoryType = ...,
        description: str = ...,
        documentVersion: str = ...,
        externalParameters: Mapping[str, SsmExternalParameterTypeDef] = ...,
        mustSucceedForCutover: bool = ...,
        operatingSystem: str = ...,
        parameters: Mapping[str, Sequence[SsmParameterStoreParameterTypeDef]] = ...,
        timeoutSeconds: int = ...,
    ) -> TemplateActionDocumentResponseTypeDef:
        """
        Put template post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.put_template_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#put_template_action)
        """

    async def remove_source_server_action(
        self, *, actionID: str, sourceServerID: str, accountID: str = ...
    ) -> Dict[str, Any]:
        """
        Remove source server post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.remove_source_server_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#remove_source_server_action)
        """

    async def remove_template_action(
        self, *, actionID: str, launchConfigurationTemplateID: str
    ) -> Dict[str, Any]:
        """
        Remove template post migration custom action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.remove_template_action)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#remove_template_action)
        """

    async def resume_replication(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Resume Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.resume_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#resume_replication)
        """

    async def retry_data_replication(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Causes the data replication initiation sequence to begin immediately upon next
        Handshake for specified SourceServer IDs, regardless of when the previous
        initiation
        started.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.retry_data_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#retry_data_replication)
        """

    async def start_cutover(
        self, *, sourceServerIDs: Sequence[str], accountID: str = ..., tags: Mapping[str, str] = ...
    ) -> StartCutoverResponseTypeDef:
        """
        Launches a Cutover Instance for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.start_cutover)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#start_cutover)
        """

    async def start_export(
        self, *, s3Bucket: str, s3Key: str, s3BucketOwner: str = ...
    ) -> StartExportResponseTypeDef:
        """
        Start export.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.start_export)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#start_export)
        """

    async def start_import(
        self, *, s3BucketSource: S3BucketSourceTypeDef, clientToken: str = ...
    ) -> StartImportResponseTypeDef:
        """
        Start import.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.start_import)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#start_import)
        """

    async def start_replication(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Starts replication for SNAPSHOT_SHIPPING agents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.start_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#start_replication)
        """

    async def start_test(
        self, *, sourceServerIDs: Sequence[str], accountID: str = ..., tags: Mapping[str, str] = ...
    ) -> StartTestResponseTypeDef:
        """
        Launches a Test Instance for specific Source Servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.start_test)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#start_test)
        """

    async def stop_replication(
        self, *, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Stop Replication.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.stop_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#stop_replication)
        """

    async def tag_resource(
        self, *, resourceArn: str, tags: Mapping[str, str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or overwrites only the specified tags for the specified Application
        Migration Service resource or
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#tag_resource)
        """

    async def terminate_target_instances(
        self, *, sourceServerIDs: Sequence[str], accountID: str = ..., tags: Mapping[str, str] = ...
    ) -> TerminateTargetInstancesResponseTypeDef:
        """
        Starts a job that terminates specific launched EC2 Test and Cutover instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.terminate_target_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#terminate_target_instances)
        """

    async def unarchive_application(
        self, *, applicationID: str, accountID: str = ...
    ) -> ApplicationResponseTypeDef:
        """
        Unarchive application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.unarchive_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#unarchive_application)
        """

    async def unarchive_wave(self, *, waveID: str, accountID: str = ...) -> WaveResponseTypeDef:
        """
        Unarchive wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.unarchive_wave)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#unarchive_wave)
        """

    async def untag_resource(
        self, *, resourceArn: str, tagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified set of tags from the specified set of Application
        Migration Service
        resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#untag_resource)
        """

    async def update_application(
        self, *, applicationID: str, accountID: str = ..., description: str = ..., name: str = ...
    ) -> ApplicationResponseTypeDef:
        """
        Update application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_application)
        """

    async def update_connector(
        self,
        *,
        connectorID: str,
        name: str = ...,
        ssmCommandConfig: ConnectorSsmCommandConfigTypeDef = ...,
    ) -> ConnectorResponseTypeDef:
        """
        Update Connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_connector)
        """

    async def update_launch_configuration(
        self,
        *,
        sourceServerID: str,
        accountID: str = ...,
        bootMode: BootModeType = ...,
        copyPrivateIp: bool = ...,
        copyTags: bool = ...,
        enableMapAutoTagging: bool = ...,
        launchDisposition: LaunchDispositionType = ...,
        licensing: LicensingTypeDef = ...,
        mapAutoTaggingMpeID: str = ...,
        name: str = ...,
        postLaunchActions: PostLaunchActionsUnionTypeDef = ...,
        targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType = ...,
    ) -> LaunchConfigurationTypeDef:
        """
        Updates multiple LaunchConfigurations by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_launch_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_launch_configuration)
        """

    async def update_launch_configuration_template(
        self,
        *,
        launchConfigurationTemplateID: str,
        associatePublicIpAddress: bool = ...,
        bootMode: BootModeType = ...,
        copyPrivateIp: bool = ...,
        copyTags: bool = ...,
        enableMapAutoTagging: bool = ...,
        largeVolumeConf: LaunchTemplateDiskConfTypeDef = ...,
        launchDisposition: LaunchDispositionType = ...,
        licensing: LicensingTypeDef = ...,
        mapAutoTaggingMpeID: str = ...,
        postLaunchActions: PostLaunchActionsUnionTypeDef = ...,
        smallVolumeConf: LaunchTemplateDiskConfTypeDef = ...,
        smallVolumeMaxSize: int = ...,
        targetInstanceTypeRightSizingMethod: TargetInstanceTypeRightSizingMethodType = ...,
    ) -> LaunchConfigurationTemplateResponseTypeDef:
        """
        Updates an existing Launch Configuration Template by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_launch_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_launch_configuration_template)
        """

    async def update_replication_configuration(
        self,
        *,
        sourceServerID: str,
        accountID: str = ...,
        associateDefaultSecurityGroup: bool = ...,
        bandwidthThrottling: int = ...,
        createPublicIP: bool = ...,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType = ...,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType = ...,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType = ...,
        ebsEncryptionKeyArn: str = ...,
        name: str = ...,
        replicatedDisks: Sequence[ReplicationConfigurationReplicatedDiskTypeDef] = ...,
        replicationServerInstanceType: str = ...,
        replicationServersSecurityGroupsIDs: Sequence[str] = ...,
        stagingAreaSubnetId: str = ...,
        stagingAreaTags: Mapping[str, str] = ...,
        useDedicatedReplicationServer: bool = ...,
        useFipsEndpoint: bool = ...,
    ) -> ReplicationConfigurationTypeDef:
        """
        Allows you to update multiple ReplicationConfigurations by Source Server ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_replication_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_replication_configuration)
        """

    async def update_replication_configuration_template(
        self,
        *,
        replicationConfigurationTemplateID: str,
        arn: str = ...,
        associateDefaultSecurityGroup: bool = ...,
        bandwidthThrottling: int = ...,
        createPublicIP: bool = ...,
        dataPlaneRouting: ReplicationConfigurationDataPlaneRoutingType = ...,
        defaultLargeStagingDiskType: ReplicationConfigurationDefaultLargeStagingDiskTypeType = ...,
        ebsEncryption: ReplicationConfigurationEbsEncryptionType = ...,
        ebsEncryptionKeyArn: str = ...,
        replicationServerInstanceType: str = ...,
        replicationServersSecurityGroupsIDs: Sequence[str] = ...,
        stagingAreaSubnetId: str = ...,
        stagingAreaTags: Mapping[str, str] = ...,
        useDedicatedReplicationServer: bool = ...,
        useFipsEndpoint: bool = ...,
    ) -> ReplicationConfigurationTemplateResponseTypeDef:
        """
        Updates multiple ReplicationConfigurationTemplates by ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_replication_configuration_template)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_replication_configuration_template)
        """

    async def update_source_server(
        self,
        *,
        sourceServerID: str,
        accountID: str = ...,
        connectorAction: SourceServerConnectorActionTypeDef = ...,
    ) -> SourceServerResponseTypeDef:
        """
        Update Source Server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_source_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_source_server)
        """

    async def update_source_server_replication_type(
        self, *, replicationType: ReplicationTypeType, sourceServerID: str, accountID: str = ...
    ) -> SourceServerResponseTypeDef:
        """
        Allows you to change between the AGENT_BASED replication type and the
        SNAPSHOT_SHIPPING replication
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_source_server_replication_type)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_source_server_replication_type)
        """

    async def update_wave(
        self, *, waveID: str, accountID: str = ..., description: str = ..., name: str = ...
    ) -> WaveResponseTypeDef:
        """
        Update wave.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.update_wave)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#update_wave)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_job_log_items"]
    ) -> DescribeJobLogItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_jobs"]) -> DescribeJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_launch_configuration_templates"]
    ) -> DescribeLaunchConfigurationTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_replication_configuration_templates"]
    ) -> DescribeReplicationConfigurationTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_source_servers"]
    ) -> DescribeSourceServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_vcenter_clients"]
    ) -> DescribeVcenterClientsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_export_errors"]
    ) -> ListExportErrorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_exports"]) -> ListExportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_import_errors"]
    ) -> ListImportErrorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_imports"]) -> ListImportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_managed_accounts"]
    ) -> ListManagedAccountsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_source_server_actions"]
    ) -> ListSourceServerActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_template_actions"]
    ) -> ListTemplateActionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_waves"]) -> ListWavesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/#get_paginator)
        """

    async def __aenter__(self) -> "MgnClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mgn.html#Mgn.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mgn/client/)
        """
