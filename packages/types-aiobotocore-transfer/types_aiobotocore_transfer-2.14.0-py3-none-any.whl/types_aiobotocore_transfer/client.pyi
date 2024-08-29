"""
Type annotations for transfer service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transfer.client import TransferClient

    session = get_session()
    async with session.create_client("transfer") as client:
        client: TransferClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    AgreementStatusTypeType,
    CertificateUsageTypeType,
    CustomStepStatusType,
    DomainType,
    EndpointTypeType,
    HomeDirectoryTypeType,
    IdentityProviderTypeType,
    ProfileTypeType,
    ProtocolType,
)
from .paginator import (
    ListAccessesPaginator,
    ListAgreementsPaginator,
    ListCertificatesPaginator,
    ListConnectorsPaginator,
    ListExecutionsPaginator,
    ListProfilesPaginator,
    ListSecurityPoliciesPaginator,
    ListServersPaginator,
    ListTagsForResourcePaginator,
    ListUsersPaginator,
    ListWorkflowsPaginator,
)
from .type_defs import (
    As2ConnectorConfigTypeDef,
    CreateAccessResponseTypeDef,
    CreateAgreementResponseTypeDef,
    CreateConnectorResponseTypeDef,
    CreateProfileResponseTypeDef,
    CreateServerResponseTypeDef,
    CreateUserResponseTypeDef,
    CreateWorkflowResponseTypeDef,
    DescribeAccessResponseTypeDef,
    DescribeAgreementResponseTypeDef,
    DescribeCertificateResponseTypeDef,
    DescribeConnectorResponseTypeDef,
    DescribeExecutionResponseTypeDef,
    DescribeHostKeyResponseTypeDef,
    DescribeProfileResponseTypeDef,
    DescribeSecurityPolicyResponseTypeDef,
    DescribeServerResponseTypeDef,
    DescribeUserResponseTypeDef,
    DescribeWorkflowResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EndpointDetailsUnionTypeDef,
    HomeDirectoryMapEntryTypeDef,
    IdentityProviderDetailsTypeDef,
    ImportCertificateResponseTypeDef,
    ImportHostKeyResponseTypeDef,
    ImportSshPublicKeyResponseTypeDef,
    ListAccessesResponseTypeDef,
    ListAgreementsResponseTypeDef,
    ListCertificatesResponseTypeDef,
    ListConnectorsResponseTypeDef,
    ListExecutionsResponseTypeDef,
    ListHostKeysResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListSecurityPoliciesResponseTypeDef,
    ListServersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUsersResponseTypeDef,
    ListWorkflowsResponseTypeDef,
    PosixProfileUnionTypeDef,
    ProtocolDetailsUnionTypeDef,
    S3StorageOptionsTypeDef,
    SftpConnectorConfigUnionTypeDef,
    StartDirectoryListingResponseTypeDef,
    StartFileTransferResponseTypeDef,
    TagTypeDef,
    TestConnectionResponseTypeDef,
    TestIdentityProviderResponseTypeDef,
    TimestampTypeDef,
    UpdateAccessResponseTypeDef,
    UpdateAgreementResponseTypeDef,
    UpdateCertificateResponseTypeDef,
    UpdateConnectorResponseTypeDef,
    UpdateHostKeyResponseTypeDef,
    UpdateProfileResponseTypeDef,
    UpdateServerResponseTypeDef,
    UpdateUserResponseTypeDef,
    WorkflowDetailsUnionTypeDef,
    WorkflowStepUnionTypeDef,
)
from .waiter import ServerOfflineWaiter, ServerOnlineWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("TransferClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class TransferClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TransferClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#close)
        """

    async def create_access(
        self,
        *,
        Role: str,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence[HomeDirectoryMapEntryTypeDef] = ...,
        Policy: str = ...,
        PosixProfile: PosixProfileUnionTypeDef = ...,
    ) -> CreateAccessResponseTypeDef:
        """
        Used by administrators to choose which groups in the directory should have
        access to upload and download files over the enabled protocols using Transfer
        Family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_access)
        """

    async def create_agreement(
        self,
        *,
        ServerId: str,
        LocalProfileId: str,
        PartnerProfileId: str,
        BaseDirectory: str,
        AccessRole: str,
        Description: str = ...,
        Status: AgreementStatusTypeType = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateAgreementResponseTypeDef:
        """
        Creates an agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_agreement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_agreement)
        """

    async def create_connector(
        self,
        *,
        Url: str,
        AccessRole: str,
        As2Config: As2ConnectorConfigTypeDef = ...,
        LoggingRole: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        SftpConfig: SftpConnectorConfigUnionTypeDef = ...,
        SecurityPolicyName: str = ...,
    ) -> CreateConnectorResponseTypeDef:
        """
        Creates the connector, which captures the parameters for a connection for the
        AS2 or SFTP
        protocol.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_connector)
        """

    async def create_profile(
        self,
        *,
        As2Id: str,
        ProfileType: ProfileTypeType,
        CertificateIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateProfileResponseTypeDef:
        """
        Creates the local or partner profile to use for AS2 transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_profile)
        """

    async def create_server(
        self,
        *,
        Certificate: str = ...,
        Domain: DomainType = ...,
        EndpointDetails: EndpointDetailsUnionTypeDef = ...,
        EndpointType: EndpointTypeType = ...,
        HostKey: str = ...,
        IdentityProviderDetails: IdentityProviderDetailsTypeDef = ...,
        IdentityProviderType: IdentityProviderTypeType = ...,
        LoggingRole: str = ...,
        PostAuthenticationLoginBanner: str = ...,
        PreAuthenticationLoginBanner: str = ...,
        Protocols: Sequence[ProtocolType] = ...,
        ProtocolDetails: ProtocolDetailsUnionTypeDef = ...,
        SecurityPolicyName: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        WorkflowDetails: WorkflowDetailsUnionTypeDef = ...,
        StructuredLogDestinations: Sequence[str] = ...,
        S3StorageOptions: S3StorageOptionsTypeDef = ...,
    ) -> CreateServerResponseTypeDef:
        """
        Instantiates an auto-scaling virtual server based on the selected file transfer
        protocol in Amazon Web
        Services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_server)
        """

    async def create_user(
        self,
        *,
        Role: str,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence[HomeDirectoryMapEntryTypeDef] = ...,
        Policy: str = ...,
        PosixProfile: PosixProfileUnionTypeDef = ...,
        SshPublicKeyBody: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user and associates them with an existing file transfer
        protocol-enabled
        server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_user)
        """

    async def create_workflow(
        self,
        *,
        Steps: Sequence[WorkflowStepUnionTypeDef],
        Description: str = ...,
        OnExceptionSteps: Sequence[WorkflowStepUnionTypeDef] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateWorkflowResponseTypeDef:
        """
        Allows you to create a workflow with specified steps and step details the
        workflow invokes after file transfer
        completes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.create_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#create_workflow)
        """

    async def delete_access(
        self, *, ServerId: str, ExternalId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Allows you to delete the access specified in the `ServerID` and `ExternalID`
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_access)
        """

    async def delete_agreement(
        self, *, AgreementId: str, ServerId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Delete the agreement that's specified in the provided `AgreementId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_agreement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_agreement)
        """

    async def delete_certificate(self, *, CertificateId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the certificate that's specified in the `CertificateId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_certificate)
        """

    async def delete_connector(self, *, ConnectorId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the connector that's specified in the provided `ConnectorId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_connector)
        """

    async def delete_host_key(
        self, *, ServerId: str, HostKeyId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the host key that's specified in the `HostKeyId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_host_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_host_key)
        """

    async def delete_profile(self, *, ProfileId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the profile that's specified in the `ProfileId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_profile)
        """

    async def delete_server(self, *, ServerId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the file transfer protocol-enabled server that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_server)
        """

    async def delete_ssh_public_key(
        self, *, ServerId: str, SshPublicKeyId: str, UserName: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a user's Secure Shell (SSH) public key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_ssh_public_key)
        """

    async def delete_user(self, *, ServerId: str, UserName: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the user belonging to a file transfer protocol-enabled server you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_user)
        """

    async def delete_workflow(self, *, WorkflowId: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.delete_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#delete_workflow)
        """

    async def describe_access(
        self, *, ServerId: str, ExternalId: str
    ) -> DescribeAccessResponseTypeDef:
        """
        Describes the access that is assigned to the specific file transfer
        protocol-enabled server, as identified by its `ServerId` property and its
        `ExternalId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_access)
        """

    async def describe_agreement(
        self, *, AgreementId: str, ServerId: str
    ) -> DescribeAgreementResponseTypeDef:
        """
        Describes the agreement that's identified by the `AgreementId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_agreement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_agreement)
        """

    async def describe_certificate(
        self, *, CertificateId: str
    ) -> DescribeCertificateResponseTypeDef:
        """
        Describes the certificate that's identified by the `CertificateId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_certificate)
        """

    async def describe_connector(self, *, ConnectorId: str) -> DescribeConnectorResponseTypeDef:
        """
        Describes the connector that's identified by the `ConnectorId.` See also: [AWS
        API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/transfer-2018-11-05/DescribeConnector).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_connector)
        """

    async def describe_execution(
        self, *, ExecutionId: str, WorkflowId: str
    ) -> DescribeExecutionResponseTypeDef:
        """
        You can use `DescribeExecution` to check the details of the execution of the
        specified
        workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_execution)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_execution)
        """

    async def describe_host_key(
        self, *, ServerId: str, HostKeyId: str
    ) -> DescribeHostKeyResponseTypeDef:
        """
        Returns the details of the host key that's specified by the `HostKeyId` and
        `ServerId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_host_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_host_key)
        """

    async def describe_profile(self, *, ProfileId: str) -> DescribeProfileResponseTypeDef:
        """
        Returns the details of the profile that's specified by the `ProfileId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_profile)
        """

    async def describe_security_policy(
        self, *, SecurityPolicyName: str
    ) -> DescribeSecurityPolicyResponseTypeDef:
        """
        Describes the security policy that is attached to your server or SFTP connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_security_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_security_policy)
        """

    async def describe_server(self, *, ServerId: str) -> DescribeServerResponseTypeDef:
        """
        Describes a file transfer protocol-enabled server that you specify by passing
        the `ServerId`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_server)
        """

    async def describe_user(self, *, ServerId: str, UserName: str) -> DescribeUserResponseTypeDef:
        """
        Describes the user assigned to the specific file transfer protocol-enabled
        server, as identified by its `ServerId`
        property.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_user)
        """

    async def describe_workflow(self, *, WorkflowId: str) -> DescribeWorkflowResponseTypeDef:
        """
        Describes the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.describe_workflow)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#describe_workflow)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#generate_presigned_url)
        """

    async def import_certificate(
        self,
        *,
        Usage: CertificateUsageTypeType,
        Certificate: str,
        CertificateChain: str = ...,
        PrivateKey: str = ...,
        ActiveDate: TimestampTypeDef = ...,
        InactiveDate: TimestampTypeDef = ...,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports the signing and encryption certificates that you need to create local
        (AS2) profiles and partner
        profiles.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.import_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#import_certificate)
        """

    async def import_host_key(
        self,
        *,
        ServerId: str,
        HostKeyBody: str,
        Description: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> ImportHostKeyResponseTypeDef:
        """
        Adds a host key to the server that's specified by the `ServerId` parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.import_host_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#import_host_key)
        """

    async def import_ssh_public_key(
        self, *, ServerId: str, SshPublicKeyBody: str, UserName: str
    ) -> ImportSshPublicKeyResponseTypeDef:
        """
        Adds a Secure Shell (SSH) public key to a Transfer Family user identified by a
        `UserName` value assigned to the specific file transfer protocol-enabled
        server, identified by
        `ServerId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.import_ssh_public_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#import_ssh_public_key)
        """

    async def list_accesses(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAccessesResponseTypeDef:
        """
        Lists the details for all the accesses you have on your server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_accesses)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_accesses)
        """

    async def list_agreements(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListAgreementsResponseTypeDef:
        """
        Returns a list of the agreements for the server that's identified by the
        `ServerId` that you
        supply.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_agreements)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_agreements)
        """

    async def list_certificates(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListCertificatesResponseTypeDef:
        """
        Returns a list of the current certificates that have been imported into
        Transfer
        Family.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_certificates)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_certificates)
        """

    async def list_connectors(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListConnectorsResponseTypeDef:
        """
        Lists the connectors for the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_connectors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_connectors)
        """

    async def list_executions(
        self, *, WorkflowId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListExecutionsResponseTypeDef:
        """
        Lists all in-progress executions for the specified workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_executions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_executions)
        """

    async def list_host_keys(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListHostKeysResponseTypeDef:
        """
        Returns a list of host keys for the server that's specified by the `ServerId`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_host_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_host_keys)
        """

    async def list_profiles(
        self, *, MaxResults: int = ..., NextToken: str = ..., ProfileType: ProfileTypeType = ...
    ) -> ListProfilesResponseTypeDef:
        """
        Returns a list of the profiles for your system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_profiles)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_profiles)
        """

    async def list_security_policies(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListSecurityPoliciesResponseTypeDef:
        """
        Lists the security policies that are attached to your servers and SFTP
        connectors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_security_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_security_policies)
        """

    async def list_servers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListServersResponseTypeDef:
        """
        Lists the file transfer protocol-enabled servers that are associated with your
        Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_servers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_servers)
        """

    async def list_tags_for_resource(
        self, *, Arn: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all of the tags associated with the Amazon Resource Name (ARN) that you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_tags_for_resource)
        """

    async def list_users(
        self, *, ServerId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists the users for a file transfer protocol-enabled server that you specify by
        passing the `ServerId`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_users)
        """

    async def list_workflows(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListWorkflowsResponseTypeDef:
        """
        Lists all workflows associated with your Amazon Web Services account for your
        current
        region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.list_workflows)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#list_workflows)
        """

    async def send_workflow_step_state(
        self, *, WorkflowId: str, ExecutionId: str, Token: str, Status: CustomStepStatusType
    ) -> Dict[str, Any]:
        """
        Sends a callback for asynchronous custom steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.send_workflow_step_state)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#send_workflow_step_state)
        """

    async def start_directory_listing(
        self,
        *,
        ConnectorId: str,
        RemoteDirectoryPath: str,
        OutputDirectoryPath: str,
        MaxItems: int = ...,
    ) -> StartDirectoryListingResponseTypeDef:
        """
        Retrieves a list of the contents of a directory from a remote SFTP server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.start_directory_listing)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#start_directory_listing)
        """

    async def start_file_transfer(
        self,
        *,
        ConnectorId: str,
        SendFilePaths: Sequence[str] = ...,
        RetrieveFilePaths: Sequence[str] = ...,
        LocalDirectoryPath: str = ...,
        RemoteDirectoryPath: str = ...,
    ) -> StartFileTransferResponseTypeDef:
        """
        Begins a file transfer between local Amazon Web Services storage and a remote
        AS2 or SFTP
        server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.start_file_transfer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#start_file_transfer)
        """

    async def start_server(self, *, ServerId: str) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a file transfer protocol-enabled server from `OFFLINE` to
        `ONLINE`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.start_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#start_server)
        """

    async def stop_server(self, *, ServerId: str) -> EmptyResponseMetadataTypeDef:
        """
        Changes the state of a file transfer protocol-enabled server from `ONLINE` to
        `OFFLINE`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.stop_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#stop_server)
        """

    async def tag_resource(
        self, *, Arn: str, Tags: Sequence[TagTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key-value pair to a resource, as identified by its Amazon Resource
        Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#tag_resource)
        """

    async def test_connection(self, *, ConnectorId: str) -> TestConnectionResponseTypeDef:
        """
        Tests whether your SFTP connector is set up successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.test_connection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#test_connection)
        """

    async def test_identity_provider(
        self,
        *,
        ServerId: str,
        UserName: str,
        ServerProtocol: ProtocolType = ...,
        SourceIp: str = ...,
        UserPassword: str = ...,
    ) -> TestIdentityProviderResponseTypeDef:
        """
        If the `IdentityProviderType` of a file transfer protocol-enabled server is
        `AWS_DIRECTORY_SERVICE` or `API_Gateway`, tests whether your identity provider
        is set up
        successfully.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.test_identity_provider)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#test_identity_provider)
        """

    async def untag_resource(
        self, *, Arn: str, TagKeys: Sequence[str]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Detaches a key-value pair from a resource, as identified by its Amazon Resource
        Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#untag_resource)
        """

    async def update_access(
        self,
        *,
        ServerId: str,
        ExternalId: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence[HomeDirectoryMapEntryTypeDef] = ...,
        Policy: str = ...,
        PosixProfile: PosixProfileUnionTypeDef = ...,
        Role: str = ...,
    ) -> UpdateAccessResponseTypeDef:
        """
        Allows you to update parameters for the access specified in the `ServerID` and
        `ExternalID`
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_access)
        """

    async def update_agreement(
        self,
        *,
        AgreementId: str,
        ServerId: str,
        Description: str = ...,
        Status: AgreementStatusTypeType = ...,
        LocalProfileId: str = ...,
        PartnerProfileId: str = ...,
        BaseDirectory: str = ...,
        AccessRole: str = ...,
    ) -> UpdateAgreementResponseTypeDef:
        """
        Updates some of the parameters for an existing agreement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_agreement)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_agreement)
        """

    async def update_certificate(
        self,
        *,
        CertificateId: str,
        ActiveDate: TimestampTypeDef = ...,
        InactiveDate: TimestampTypeDef = ...,
        Description: str = ...,
    ) -> UpdateCertificateResponseTypeDef:
        """
        Updates the active and inactive dates for a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_certificate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_certificate)
        """

    async def update_connector(
        self,
        *,
        ConnectorId: str,
        Url: str = ...,
        As2Config: As2ConnectorConfigTypeDef = ...,
        AccessRole: str = ...,
        LoggingRole: str = ...,
        SftpConfig: SftpConnectorConfigUnionTypeDef = ...,
        SecurityPolicyName: str = ...,
    ) -> UpdateConnectorResponseTypeDef:
        """
        Updates some of the parameters for an existing connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_connector)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_connector)
        """

    async def update_host_key(
        self, *, ServerId: str, HostKeyId: str, Description: str
    ) -> UpdateHostKeyResponseTypeDef:
        """
        Updates the description for the host key that's specified by the `ServerId` and
        `HostKeyId`
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_host_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_host_key)
        """

    async def update_profile(
        self, *, ProfileId: str, CertificateIds: Sequence[str] = ...
    ) -> UpdateProfileResponseTypeDef:
        """
        Updates some of the parameters for an existing profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_profile)
        """

    async def update_server(
        self,
        *,
        ServerId: str,
        Certificate: str = ...,
        ProtocolDetails: ProtocolDetailsUnionTypeDef = ...,
        EndpointDetails: EndpointDetailsUnionTypeDef = ...,
        EndpointType: EndpointTypeType = ...,
        HostKey: str = ...,
        IdentityProviderDetails: IdentityProviderDetailsTypeDef = ...,
        LoggingRole: str = ...,
        PostAuthenticationLoginBanner: str = ...,
        PreAuthenticationLoginBanner: str = ...,
        Protocols: Sequence[ProtocolType] = ...,
        SecurityPolicyName: str = ...,
        WorkflowDetails: WorkflowDetailsUnionTypeDef = ...,
        StructuredLogDestinations: Sequence[str] = ...,
        S3StorageOptions: S3StorageOptionsTypeDef = ...,
    ) -> UpdateServerResponseTypeDef:
        """
        Updates the file transfer protocol-enabled server's properties after that
        server has been
        created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_server)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_server)
        """

    async def update_user(
        self,
        *,
        ServerId: str,
        UserName: str,
        HomeDirectory: str = ...,
        HomeDirectoryType: HomeDirectoryTypeType = ...,
        HomeDirectoryMappings: Sequence[HomeDirectoryMapEntryTypeDef] = ...,
        Policy: str = ...,
        PosixProfile: PosixProfileUnionTypeDef = ...,
        Role: str = ...,
    ) -> UpdateUserResponseTypeDef:
        """
        Assigns new properties to a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_accesses"]) -> ListAccessesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_agreements"]) -> ListAgreementsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_connectors"]) -> ListConnectorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_executions"]) -> ListExecutionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_profiles"]) -> ListProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_security_policies"]
    ) -> ListSecurityPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_servers"]) -> ListServersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_workflows"]) -> ListWorkflowsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_offline"]) -> ServerOfflineWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["server_online"]) -> ServerOnlineWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/#get_waiter)
        """

    async def __aenter__(self) -> "TransferClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transfer.html#Transfer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transfer/client/)
        """
