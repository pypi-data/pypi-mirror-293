"""
Type annotations for datasync service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_datasync.client import DataSyncClient

    session = get_session()
    async with session.create_client("datasync") as client:
        client: DataSyncClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AzureAccessTierType,
    DiscoveryResourceTypeType,
    EfsInTransitEncryptionType,
    HdfsAuthenticationTypeType,
    ObjectStorageServerProtocolType,
    S3StorageClassType,
)
from .paginator import (
    DescribeStorageSystemResourceMetricsPaginator,
    ListAgentsPaginator,
    ListDiscoveryJobsPaginator,
    ListLocationsPaginator,
    ListStorageSystemsPaginator,
    ListTagsForResourcePaginator,
    ListTaskExecutionsPaginator,
    ListTasksPaginator,
)
from .type_defs import (
    AddStorageSystemResponseTypeDef,
    AzureBlobSasConfigurationTypeDef,
    BlobTypeDef,
    CreateAgentResponseTypeDef,
    CreateLocationAzureBlobResponseTypeDef,
    CreateLocationEfsResponseTypeDef,
    CreateLocationFsxLustreResponseTypeDef,
    CreateLocationFsxOntapResponseTypeDef,
    CreateLocationFsxOpenZfsResponseTypeDef,
    CreateLocationFsxWindowsResponseTypeDef,
    CreateLocationHdfsResponseTypeDef,
    CreateLocationNfsResponseTypeDef,
    CreateLocationObjectStorageResponseTypeDef,
    CreateLocationS3ResponseTypeDef,
    CreateLocationSmbResponseTypeDef,
    CreateTaskResponseTypeDef,
    CredentialsTypeDef,
    DescribeAgentResponseTypeDef,
    DescribeDiscoveryJobResponseTypeDef,
    DescribeLocationAzureBlobResponseTypeDef,
    DescribeLocationEfsResponseTypeDef,
    DescribeLocationFsxLustreResponseTypeDef,
    DescribeLocationFsxOntapResponseTypeDef,
    DescribeLocationFsxOpenZfsResponseTypeDef,
    DescribeLocationFsxWindowsResponseTypeDef,
    DescribeLocationHdfsResponseTypeDef,
    DescribeLocationNfsResponseTypeDef,
    DescribeLocationObjectStorageResponseTypeDef,
    DescribeLocationS3ResponseTypeDef,
    DescribeLocationSmbResponseTypeDef,
    DescribeStorageSystemResourceMetricsResponseTypeDef,
    DescribeStorageSystemResourcesResponseTypeDef,
    DescribeStorageSystemResponseTypeDef,
    DescribeTaskExecutionResponseTypeDef,
    DescribeTaskResponseTypeDef,
    DiscoveryServerConfigurationTypeDef,
    Ec2ConfigUnionTypeDef,
    FilterRuleTypeDef,
    FsxProtocolTypeDef,
    HdfsNameNodeTypeDef,
    ListAgentsResponseTypeDef,
    ListDiscoveryJobsResponseTypeDef,
    ListLocationsResponseTypeDef,
    ListStorageSystemsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTaskExecutionsResponseTypeDef,
    ListTasksResponseTypeDef,
    LocationFilterTypeDef,
    ManifestConfigTypeDef,
    NfsMountOptionsTypeDef,
    OnPremConfigUnionTypeDef,
    OptionsTypeDef,
    QopConfigurationTypeDef,
    S3ConfigTypeDef,
    SmbMountOptionsTypeDef,
    StartDiscoveryJobResponseTypeDef,
    StartTaskExecutionResponseTypeDef,
    TagListEntryTypeDef,
    TaskFilterTypeDef,
    TaskReportConfigTypeDef,
    TaskScheduleTypeDef,
    TimestampTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("DataSyncClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    InternalException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]

class DataSyncClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        DataSyncClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#exceptions)
        """

    async def add_storage_system(
        self,
        *,
        ServerConfiguration: DiscoveryServerConfigurationTypeDef,
        SystemType: Literal["NetAppONTAP"],
        AgentArns: Sequence[str],
        ClientToken: str,
        Credentials: CredentialsTypeDef,
        CloudWatchLogGroupArn: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        Name: str = ...,
    ) -> AddStorageSystemResponseTypeDef:
        """
        Creates an Amazon Web Services resource for an on-premises storage system that
        you want DataSync Discovery to collect information
        about.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.add_storage_system)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#add_storage_system)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#can_paginate)
        """

    async def cancel_task_execution(self, *, TaskExecutionArn: str) -> Dict[str, Any]:
        """
        Stops an DataSync task execution that's in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.cancel_task_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#cancel_task_execution)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#close)
        """

    async def create_agent(
        self,
        *,
        ActivationKey: str,
        AgentName: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        VpcEndpointId: str = ...,
        SubnetArns: Sequence[str] = ...,
        SecurityGroupArns: Sequence[str] = ...,
    ) -> CreateAgentResponseTypeDef:
        """
        Activates an DataSync agent that you've deployed in your storage environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_agent)
        """

    async def create_location_azure_blob(
        self,
        *,
        ContainerUrl: str,
        AuthenticationType: Literal["SAS"],
        AgentArns: Sequence[str],
        SasConfiguration: AzureBlobSasConfigurationTypeDef = ...,
        BlobType: Literal["BLOCK"] = ...,
        AccessTier: AzureAccessTierType = ...,
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationAzureBlobResponseTypeDef:
        """
        Creates a transfer *location* for a Microsoft Azure Blob Storage container.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_azure_blob)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_azure_blob)
        """

    async def create_location_efs(
        self,
        *,
        EfsFilesystemArn: str,
        Ec2Config: Ec2ConfigUnionTypeDef,
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        AccessPointArn: str = ...,
        FileSystemAccessRoleArn: str = ...,
        InTransitEncryption: EfsInTransitEncryptionType = ...,
    ) -> CreateLocationEfsResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon EFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_efs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_efs)
        """

    async def create_location_fsx_lustre(
        self,
        *,
        FsxFilesystemArn: str,
        SecurityGroupArns: Sequence[str],
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationFsxLustreResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon FSx for Lustre file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_fsx_lustre)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_fsx_lustre)
        """

    async def create_location_fsx_ontap(
        self,
        *,
        Protocol: FsxProtocolTypeDef,
        SecurityGroupArns: Sequence[str],
        StorageVirtualMachineArn: str,
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationFsxOntapResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon FSx for NetApp ONTAP file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_fsx_ontap)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_fsx_ontap)
        """

    async def create_location_fsx_open_zfs(
        self,
        *,
        FsxFilesystemArn: str,
        Protocol: FsxProtocolTypeDef,
        SecurityGroupArns: Sequence[str],
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationFsxOpenZfsResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon FSx for OpenZFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_fsx_open_zfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_fsx_open_zfs)
        """

    async def create_location_fsx_windows(
        self,
        *,
        FsxFilesystemArn: str,
        SecurityGroupArns: Sequence[str],
        User: str,
        Password: str,
        Subdirectory: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        Domain: str = ...,
    ) -> CreateLocationFsxWindowsResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon FSx for Windows File Server file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_fsx_windows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_fsx_windows)
        """

    async def create_location_hdfs(
        self,
        *,
        NameNodes: Sequence[HdfsNameNodeTypeDef],
        AuthenticationType: HdfsAuthenticationTypeType,
        AgentArns: Sequence[str],
        Subdirectory: str = ...,
        BlockSize: int = ...,
        ReplicationFactor: int = ...,
        KmsKeyProviderUri: str = ...,
        QopConfiguration: QopConfigurationTypeDef = ...,
        SimpleUser: str = ...,
        KerberosPrincipal: str = ...,
        KerberosKeytab: BlobTypeDef = ...,
        KerberosKrb5Conf: BlobTypeDef = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationHdfsResponseTypeDef:
        """
        Creates a transfer *location* for a Hadoop Distributed File System (HDFS).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_hdfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_hdfs)
        """

    async def create_location_nfs(
        self,
        *,
        Subdirectory: str,
        ServerHostname: str,
        OnPremConfig: OnPremConfigUnionTypeDef,
        MountOptions: NfsMountOptionsTypeDef = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationNfsResponseTypeDef:
        """
        Creates a transfer *location* for a Network File System (NFS) file server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_nfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_nfs)
        """

    async def create_location_object_storage(
        self,
        *,
        ServerHostname: str,
        BucketName: str,
        AgentArns: Sequence[str],
        ServerPort: int = ...,
        ServerProtocol: ObjectStorageServerProtocolType = ...,
        Subdirectory: str = ...,
        AccessKey: str = ...,
        SecretKey: str = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        ServerCertificate: BlobTypeDef = ...,
    ) -> CreateLocationObjectStorageResponseTypeDef:
        """
        Creates a transfer *location* for an object storage system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_object_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_object_storage)
        """

    async def create_location_s3(
        self,
        *,
        S3BucketArn: str,
        S3Config: S3ConfigTypeDef,
        Subdirectory: str = ...,
        S3StorageClass: S3StorageClassType = ...,
        AgentArns: Sequence[str] = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationS3ResponseTypeDef:
        """
        Creates a transfer *location* for an Amazon S3 bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_s3)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_s3)
        """

    async def create_location_smb(
        self,
        *,
        Subdirectory: str,
        ServerHostname: str,
        User: str,
        Password: str,
        AgentArns: Sequence[str],
        Domain: str = ...,
        MountOptions: SmbMountOptionsTypeDef = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> CreateLocationSmbResponseTypeDef:
        """
        Creates a transfer *location* for a Server Message Block (SMB) file server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_location_smb)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_location_smb)
        """

    async def create_task(
        self,
        *,
        SourceLocationArn: str,
        DestinationLocationArn: str,
        CloudWatchLogGroupArn: str = ...,
        Name: str = ...,
        Options: OptionsTypeDef = ...,
        Excludes: Sequence[FilterRuleTypeDef] = ...,
        Schedule: TaskScheduleTypeDef = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
        Includes: Sequence[FilterRuleTypeDef] = ...,
        ManifestConfig: ManifestConfigTypeDef = ...,
        TaskReportConfig: TaskReportConfigTypeDef = ...,
    ) -> CreateTaskResponseTypeDef:
        """
        Configures a *task*, which defines where and how DataSync transfers your data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.create_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#create_task)
        """

    async def delete_agent(self, *, AgentArn: str) -> Dict[str, Any]:
        """
        Removes an DataSync agent resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.delete_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#delete_agent)
        """

    async def delete_location(self, *, LocationArn: str) -> Dict[str, Any]:
        """
        Deletes a transfer location resource from DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.delete_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#delete_location)
        """

    async def delete_task(self, *, TaskArn: str) -> Dict[str, Any]:
        """
        Deletes a transfer task resource from DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.delete_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#delete_task)
        """

    async def describe_agent(self, *, AgentArn: str) -> DescribeAgentResponseTypeDef:
        """
        Returns information about an DataSync agent, such as its name, service endpoint
        type, and
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_agent)
        """

    async def describe_discovery_job(
        self, *, DiscoveryJobArn: str
    ) -> DescribeDiscoveryJobResponseTypeDef:
        """
        Returns information about a DataSync discovery job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_discovery_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_discovery_job)
        """

    async def describe_location_azure_blob(
        self, *, LocationArn: str
    ) -> DescribeLocationAzureBlobResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for Microsoft Azure
        Blob Storage is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_azure_blob)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_azure_blob)
        """

    async def describe_location_efs(
        self, *, LocationArn: str
    ) -> DescribeLocationEfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon EFS file
        system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_efs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_efs)
        """

    async def describe_location_fsx_lustre(
        self, *, LocationArn: str
    ) -> DescribeLocationFsxLustreResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        Lustre file system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_fsx_lustre)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_fsx_lustre)
        """

    async def describe_location_fsx_ontap(
        self, *, LocationArn: str
    ) -> DescribeLocationFsxOntapResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        NetApp ONTAP file system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_fsx_ontap)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_fsx_ontap)
        """

    async def describe_location_fsx_open_zfs(
        self, *, LocationArn: str
    ) -> DescribeLocationFsxOpenZfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        OpenZFS file system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_fsx_open_zfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_fsx_open_zfs)
        """

    async def describe_location_fsx_windows(
        self, *, LocationArn: str
    ) -> DescribeLocationFsxWindowsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an Amazon FSx for
        Windows File Server file system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_fsx_windows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_fsx_windows)
        """

    async def describe_location_hdfs(
        self, *, LocationArn: str
    ) -> DescribeLocationHdfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Hadoop
        Distributed File System (HDFS) is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_hdfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_hdfs)
        """

    async def describe_location_nfs(
        self, *, LocationArn: str
    ) -> DescribeLocationNfsResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Network File
        System (NFS) file server is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_nfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_nfs)
        """

    async def describe_location_object_storage(
        self, *, LocationArn: str
    ) -> DescribeLocationObjectStorageResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an object storage
        system is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_object_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_object_storage)
        """

    async def describe_location_s3(self, *, LocationArn: str) -> DescribeLocationS3ResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for an S3 bucket is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_s3)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_s3)
        """

    async def describe_location_smb(
        self, *, LocationArn: str
    ) -> DescribeLocationSmbResponseTypeDef:
        """
        Provides details about how an DataSync transfer location for a Server Message
        Block (SMB) file server is
        configured.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_location_smb)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_location_smb)
        """

    async def describe_storage_system(
        self, *, StorageSystemArn: str
    ) -> DescribeStorageSystemResponseTypeDef:
        """
        Returns information about an on-premises storage system that you're using with
        DataSync
        Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_storage_system)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_storage_system)
        """

    async def describe_storage_system_resource_metrics(
        self,
        *,
        DiscoveryJobArn: str,
        ResourceType: DiscoveryResourceTypeType,
        ResourceId: str,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeStorageSystemResourceMetricsResponseTypeDef:
        """
        Returns information, including performance data and capacity usage, which
        DataSync Discovery collects about a specific resource in your-premises storage
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_storage_system_resource_metrics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_storage_system_resource_metrics)
        """

    async def describe_storage_system_resources(
        self,
        *,
        DiscoveryJobArn: str,
        ResourceType: DiscoveryResourceTypeType,
        ResourceIds: Sequence[str] = ...,
        Filter: Mapping[Literal["SVM"], Sequence[str]] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeStorageSystemResourcesResponseTypeDef:
        """
        Returns information that DataSync Discovery collects about resources in your
        on-premises storage
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_storage_system_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_storage_system_resources)
        """

    async def describe_task(self, *, TaskArn: str) -> DescribeTaskResponseTypeDef:
        """
        Provides information about a *task*, which defines where and how DataSync
        transfers your
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_task)
        """

    async def describe_task_execution(
        self, *, TaskExecutionArn: str
    ) -> DescribeTaskExecutionResponseTypeDef:
        """
        Provides information about an execution of your DataSync task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.describe_task_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#describe_task_execution)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#generate_presigned_url)
        """

    async def generate_recommendations(
        self,
        *,
        DiscoveryJobArn: str,
        ResourceIds: Sequence[str],
        ResourceType: DiscoveryResourceTypeType,
    ) -> Dict[str, Any]:
        """
        Creates recommendations about where to migrate your data to in Amazon Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.generate_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#generate_recommendations)
        """

    async def list_agents(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAgentsResponseTypeDef:
        """
        Returns a list of DataSync agents that belong to an Amazon Web Services account
        in the Amazon Web Services Region specified in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_agents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_agents)
        """

    async def list_discovery_jobs(
        self, *, StorageSystemArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListDiscoveryJobsResponseTypeDef:
        """
        Provides a list of the existing discovery jobs in the Amazon Web Services
        Region and Amazon Web Services account where you're using DataSync
        Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_discovery_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_discovery_jobs)
        """

    async def list_locations(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[LocationFilterTypeDef] = ...,
    ) -> ListLocationsResponseTypeDef:
        """
        Returns a list of source and destination locations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_locations)
        """

    async def list_storage_systems(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListStorageSystemsResponseTypeDef:
        """
        Lists the on-premises storage systems that you're using with DataSync Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_storage_systems)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_storage_systems)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns all the tags associated with an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_tags_for_resource)
        """

    async def list_task_executions(
        self, *, TaskArn: str = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> ListTaskExecutionsResponseTypeDef:
        """
        Returns a list of executions for an DataSync transfer task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_task_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_task_executions)
        """

    async def list_tasks(
        self,
        *,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[TaskFilterTypeDef] = ...,
    ) -> ListTasksResponseTypeDef:
        """
        Returns a list of the DataSync tasks you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.list_tasks)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#list_tasks)
        """

    async def remove_storage_system(self, *, StorageSystemArn: str) -> Dict[str, Any]:
        """
        Permanently removes a storage system resource from DataSync Discovery,
        including the associated discovery jobs, collected data, and
        recommendations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.remove_storage_system)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#remove_storage_system)
        """

    async def start_discovery_job(
        self,
        *,
        StorageSystemArn: str,
        CollectionDurationMinutes: int,
        ClientToken: str,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> StartDiscoveryJobResponseTypeDef:
        """
        Runs a DataSync discovery job on your on-premises storage system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.start_discovery_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#start_discovery_job)
        """

    async def start_task_execution(
        self,
        *,
        TaskArn: str,
        OverrideOptions: OptionsTypeDef = ...,
        Includes: Sequence[FilterRuleTypeDef] = ...,
        Excludes: Sequence[FilterRuleTypeDef] = ...,
        ManifestConfig: ManifestConfigTypeDef = ...,
        TaskReportConfig: TaskReportConfigTypeDef = ...,
        Tags: Sequence[TagListEntryTypeDef] = ...,
    ) -> StartTaskExecutionResponseTypeDef:
        """
        Starts an DataSync transfer task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.start_task_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#start_task_execution)
        """

    async def stop_discovery_job(self, *, DiscoveryJobArn: str) -> Dict[str, Any]:
        """
        Stops a running DataSync discovery job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.stop_discovery_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#stop_discovery_job)
        """

    async def tag_resource(
        self, *, ResourceArn: str, Tags: Sequence[TagListEntryTypeDef]
    ) -> Dict[str, Any]:
        """
        Applies a *tag* to an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, Keys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#untag_resource)
        """

    async def update_agent(self, *, AgentArn: str, Name: str = ...) -> Dict[str, Any]:
        """
        Updates the name of an DataSync agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_agent)
        """

    async def update_discovery_job(
        self, *, DiscoveryJobArn: str, CollectionDurationMinutes: int
    ) -> Dict[str, Any]:
        """
        Edits a DataSync discovery job configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_discovery_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_discovery_job)
        """

    async def update_location_azure_blob(
        self,
        *,
        LocationArn: str,
        Subdirectory: str = ...,
        AuthenticationType: Literal["SAS"] = ...,
        SasConfiguration: AzureBlobSasConfigurationTypeDef = ...,
        BlobType: Literal["BLOCK"] = ...,
        AccessTier: AzureAccessTierType = ...,
        AgentArns: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of the Microsoft Azure Blob Storage transfer
        location that you're using with
        DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_location_azure_blob)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_location_azure_blob)
        """

    async def update_location_hdfs(
        self,
        *,
        LocationArn: str,
        Subdirectory: str = ...,
        NameNodes: Sequence[HdfsNameNodeTypeDef] = ...,
        BlockSize: int = ...,
        ReplicationFactor: int = ...,
        KmsKeyProviderUri: str = ...,
        QopConfiguration: QopConfigurationTypeDef = ...,
        AuthenticationType: HdfsAuthenticationTypeType = ...,
        SimpleUser: str = ...,
        KerberosPrincipal: str = ...,
        KerberosKeytab: BlobTypeDef = ...,
        KerberosKrb5Conf: BlobTypeDef = ...,
        AgentArns: Sequence[str] = ...,
    ) -> Dict[str, Any]:
        """
        Updates some parameters of a previously created location for a Hadoop
        Distributed File System
        cluster.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_location_hdfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_location_hdfs)
        """

    async def update_location_nfs(
        self,
        *,
        LocationArn: str,
        Subdirectory: str = ...,
        OnPremConfig: OnPremConfigUnionTypeDef = ...,
        MountOptions: NfsMountOptionsTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of the Network File System (NFS) transfer location
        that you're using with
        DataSync.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_location_nfs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_location_nfs)
        """

    async def update_location_object_storage(
        self,
        *,
        LocationArn: str,
        ServerPort: int = ...,
        ServerProtocol: ObjectStorageServerProtocolType = ...,
        Subdirectory: str = ...,
        AccessKey: str = ...,
        SecretKey: str = ...,
        AgentArns: Sequence[str] = ...,
        ServerCertificate: BlobTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates some parameters of an existing DataSync location for an object storage
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_location_object_storage)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_location_object_storage)
        """

    async def update_location_smb(
        self,
        *,
        LocationArn: str,
        Subdirectory: str = ...,
        User: str = ...,
        Domain: str = ...,
        Password: str = ...,
        AgentArns: Sequence[str] = ...,
        MountOptions: SmbMountOptionsTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates some of the parameters of a Server Message Block (SMB) file server
        location that you can use for DataSync
        transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_location_smb)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_location_smb)
        """

    async def update_storage_system(
        self,
        *,
        StorageSystemArn: str,
        ServerConfiguration: DiscoveryServerConfigurationTypeDef = ...,
        AgentArns: Sequence[str] = ...,
        Name: str = ...,
        CloudWatchLogGroupArn: str = ...,
        Credentials: CredentialsTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Modifies some configurations of an on-premises storage system resource that
        you're using with DataSync
        Discovery.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_storage_system)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_storage_system)
        """

    async def update_task(
        self,
        *,
        TaskArn: str,
        Options: OptionsTypeDef = ...,
        Excludes: Sequence[FilterRuleTypeDef] = ...,
        Schedule: TaskScheduleTypeDef = ...,
        Name: str = ...,
        CloudWatchLogGroupArn: str = ...,
        Includes: Sequence[FilterRuleTypeDef] = ...,
        ManifestConfig: ManifestConfigTypeDef = ...,
        TaskReportConfig: TaskReportConfigTypeDef = ...,
    ) -> Dict[str, Any]:
        """
        Updates the configuration of a *task*, which defines where and how DataSync
        transfers your
        data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_task)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_task)
        """

    async def update_task_execution(
        self, *, TaskExecutionArn: str, Options: OptionsTypeDef
    ) -> Dict[str, Any]:
        """
        Updates the configuration of a running DataSync task execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.update_task_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#update_task_execution)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_storage_system_resource_metrics"]
    ) -> DescribeStorageSystemResourceMetricsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agents"]) -> ListAgentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_discovery_jobs"]
    ) -> ListDiscoveryJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_locations"]) -> ListLocationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_storage_systems"]
    ) -> ListStorageSystemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_task_executions"]
    ) -> ListTaskExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_tasks"]) -> ListTasksPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/#get_paginator)
        """

    async def __aenter__(self) -> "DataSyncClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/datasync.html#DataSync.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_datasync/client/)
        """
