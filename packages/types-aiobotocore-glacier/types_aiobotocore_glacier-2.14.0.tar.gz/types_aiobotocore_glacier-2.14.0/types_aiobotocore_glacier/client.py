"""
Type annotations for glacier service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_glacier.client import GlacierClient

    session = get_session()
    async with session.create_client("glacier") as client:
        client: GlacierClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListJobsPaginator,
    ListMultipartUploadsPaginator,
    ListPartsPaginator,
    ListVaultsPaginator,
)
from .type_defs import (
    ArchiveCreationOutputTypeDef,
    BlobTypeDef,
    CreateVaultOutputTypeDef,
    DataRetrievalPolicyUnionTypeDef,
    DescribeVaultResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDataRetrievalPolicyOutputTypeDef,
    GetJobOutputOutputTypeDef,
    GetVaultAccessPolicyOutputTypeDef,
    GetVaultLockOutputTypeDef,
    GetVaultNotificationsOutputTypeDef,
    GlacierJobDescriptionResponseTypeDef,
    InitiateJobOutputTypeDef,
    InitiateMultipartUploadOutputTypeDef,
    InitiateVaultLockOutputTypeDef,
    JobParametersTypeDef,
    ListJobsOutputTypeDef,
    ListMultipartUploadsOutputTypeDef,
    ListPartsOutputTypeDef,
    ListProvisionedCapacityOutputTypeDef,
    ListTagsForVaultOutputTypeDef,
    ListVaultsOutputTypeDef,
    PurchaseProvisionedCapacityOutputTypeDef,
    UploadMultipartPartOutputTypeDef,
    VaultAccessPolicyTypeDef,
    VaultLockPolicyTypeDef,
    VaultNotificationConfigUnionTypeDef,
)
from .waiter import VaultExistsWaiter, VaultNotExistsWaiter

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("GlacierClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    InsufficientCapacityException: Type[BotocoreClientError]
    InvalidParameterValueException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MissingParameterValueException: Type[BotocoreClientError]
    PolicyEnforcedException: Type[BotocoreClientError]
    RequestTimeoutException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]


class GlacierClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GlacierClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#exceptions)
        """

    async def abort_multipart_upload(
        self, *, vaultName: str, uploadId: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation aborts a multipart upload identified by the upload ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.abort_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#abort_multipart_upload)
        """

    async def abort_vault_lock(
        self, *, vaultName: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation aborts the vault locking process if the vault lock is not in the
        `Locked`
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.abort_vault_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#abort_vault_lock)
        """

    async def add_tags_to_vault(
        self, *, vaultName: str, accountId: str = "-", Tags: Mapping[str, str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation adds the specified tags to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.add_tags_to_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#add_tags_to_vault)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#close)
        """

    async def complete_multipart_upload(
        self,
        *,
        vaultName: str,
        uploadId: str,
        accountId: str = "-",
        archiveSize: str = ...,
        checksum: str = ...,
    ) -> ArchiveCreationOutputTypeDef:
        """
        You call this operation to inform Amazon S3 Glacier (Glacier) that all the
        archive parts have been uploaded and that Glacier can now assemble the archive
        from the uploaded
        parts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.complete_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#complete_multipart_upload)
        """

    async def complete_vault_lock(
        self, *, vaultName: str, lockId: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation completes the vault locking process by transitioning the vault
        lock from the `InProgress` state to the `Locked` state, which causes the vault
        lock policy to become
        unchangeable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.complete_vault_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#complete_vault_lock)
        """

    async def create_vault(
        self, *, vaultName: str, accountId: str = "-"
    ) -> CreateVaultOutputTypeDef:
        """
        This operation creates a new vault with the specified name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.create_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#create_vault)
        """

    async def delete_archive(
        self, *, vaultName: str, archiveId: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes an archive from a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.delete_archive)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#delete_archive)
        """

    async def delete_vault(
        self, *, vaultName: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.delete_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#delete_vault)
        """

    async def delete_vault_access_policy(
        self, *, vaultName: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes the access policy associated with the specified vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.delete_vault_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#delete_vault_access_policy)
        """

    async def delete_vault_notifications(
        self, *, vaultName: str, accountId: str = "-"
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation deletes the notification configuration set for a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.delete_vault_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#delete_vault_notifications)
        """

    async def describe_job(
        self, *, vaultName: str, jobId: str, accountId: str = "-"
    ) -> GlacierJobDescriptionResponseTypeDef:
        """
        This operation returns information about a job you previously initiated,
        including the job initiation date, the user who initiated the job, the job
        status code/message and the Amazon SNS topic to notify after Amazon S3 Glacier
        (Glacier) completes the
        job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#describe_job)
        """

    async def describe_vault(
        self, *, vaultName: str, accountId: str = "-"
    ) -> DescribeVaultResponseTypeDef:
        """
        This operation returns information about a vault, including the vault's Amazon
        Resource Name (ARN), the date the vault was created, the number of archives it
        contains, and the total size of all the archives in the
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.describe_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#describe_vault)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#generate_presigned_url)
        """

    async def get_data_retrieval_policy(
        self, *, accountId: str = "-"
    ) -> GetDataRetrievalPolicyOutputTypeDef:
        """
        This operation returns the current data retrieval policy for the account and
        region specified in the GET
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_data_retrieval_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_data_retrieval_policy)
        """

    async def get_job_output(
        self, *, vaultName: str, jobId: str, accountId: str = "-", range: str = ...
    ) -> GetJobOutputOutputTypeDef:
        """
        This operation downloads the output of the job you initiated using  InitiateJob.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_job_output)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_job_output)
        """

    async def get_vault_access_policy(
        self, *, vaultName: str, accountId: str = "-"
    ) -> GetVaultAccessPolicyOutputTypeDef:
        """
        This operation retrieves the `access-policy` subresource set on the vault; for
        more information on setting this subresource, see [Set Vault Access Policy (PUT
        access-policy)](https://docs.aws.amazon.com/amazonglacier/latest/dev/api-SetVaultAccessPolicy.html).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_vault_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_vault_access_policy)
        """

    async def get_vault_lock(
        self, *, vaultName: str, accountId: str = "-"
    ) -> GetVaultLockOutputTypeDef:
        """
        This operation retrieves the following attributes from the `lock-policy`
        subresource set on the specified vault: * The vault lock policy set on the
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_vault_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_vault_lock)
        """

    async def get_vault_notifications(
        self, *, vaultName: str, accountId: str = "-"
    ) -> GetVaultNotificationsOutputTypeDef:
        """
        This operation retrieves the `notification-configuration` subresource of the
        specified
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_vault_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_vault_notifications)
        """

    async def initiate_job(
        self, *, vaultName: str, accountId: str = "-", jobParameters: JobParametersTypeDef = ...
    ) -> InitiateJobOutputTypeDef:
        """
        This operation initiates a job of the specified type, which can be a select, an
        archival retrieval, or a vault
        retrieval.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.initiate_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#initiate_job)
        """

    async def initiate_multipart_upload(
        self,
        *,
        vaultName: str,
        accountId: str = "-",
        archiveDescription: str = ...,
        partSize: str = ...,
    ) -> InitiateMultipartUploadOutputTypeDef:
        """
        This operation initiates a multipart upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.initiate_multipart_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#initiate_multipart_upload)
        """

    async def initiate_vault_lock(
        self, *, vaultName: str, accountId: str = "-", policy: VaultLockPolicyTypeDef = ...
    ) -> InitiateVaultLockOutputTypeDef:
        """
        This operation initiates the vault locking process by doing the following: *
        Installing a vault lock policy on the specified
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.initiate_vault_lock)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#initiate_vault_lock)
        """

    async def list_jobs(
        self,
        *,
        vaultName: str,
        accountId: str = "-",
        limit: str = ...,
        marker: str = ...,
        statuscode: str = ...,
        completed: str = ...,
    ) -> ListJobsOutputTypeDef:
        """
        This operation lists jobs for a vault, including jobs that are in-progress and
        jobs that have recently
        finished.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_jobs)
        """

    async def list_multipart_uploads(
        self, *, vaultName: str, accountId: str = "-", marker: str = ..., limit: str = ...
    ) -> ListMultipartUploadsOutputTypeDef:
        """
        This operation lists in-progress multipart uploads for the specified vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_multipart_uploads)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_multipart_uploads)
        """

    async def list_parts(
        self,
        *,
        vaultName: str,
        uploadId: str,
        accountId: str = "-",
        marker: str = ...,
        limit: str = ...,
    ) -> ListPartsOutputTypeDef:
        """
        This operation lists the parts of an archive that have been uploaded in a
        specific multipart
        upload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_parts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_parts)
        """

    async def list_provisioned_capacity(
        self, *, accountId: str = "-"
    ) -> ListProvisionedCapacityOutputTypeDef:
        """
        This operation lists the provisioned capacity units for the specified AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_provisioned_capacity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_provisioned_capacity)
        """

    async def list_tags_for_vault(
        self, *, vaultName: str, accountId: str = "-"
    ) -> ListTagsForVaultOutputTypeDef:
        """
        This operation lists all the tags attached to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_tags_for_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_tags_for_vault)
        """

    async def list_vaults(
        self, *, accountId: str = "-", marker: str = ..., limit: str = ...
    ) -> ListVaultsOutputTypeDef:
        """
        This operation lists all vaults owned by the calling user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.list_vaults)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#list_vaults)
        """

    async def purchase_provisioned_capacity(
        self, *, accountId: str = "-"
    ) -> PurchaseProvisionedCapacityOutputTypeDef:
        """
        This operation purchases a provisioned capacity unit for an AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.purchase_provisioned_capacity)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#purchase_provisioned_capacity)
        """

    async def remove_tags_from_vault(
        self, *, vaultName: str, accountId: str = "-", TagKeys: Sequence[str] = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation removes one or more tags from the set of tags attached to a
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.remove_tags_from_vault)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#remove_tags_from_vault)
        """

    async def set_data_retrieval_policy(
        self, *, accountId: str = "-", Policy: DataRetrievalPolicyUnionTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation sets and then enacts a data retrieval policy in the region
        specified in the PUT
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.set_data_retrieval_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#set_data_retrieval_policy)
        """

    async def set_vault_access_policy(
        self, *, vaultName: str, accountId: str = "-", policy: VaultAccessPolicyTypeDef = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation configures an access policy for a vault and will overwrite an
        existing
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.set_vault_access_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#set_vault_access_policy)
        """

    async def set_vault_notifications(
        self,
        *,
        vaultName: str,
        accountId: str = "-",
        vaultNotificationConfig: VaultNotificationConfigUnionTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        This operation configures notifications that will be sent when specific events
        happen to a
        vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.set_vault_notifications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#set_vault_notifications)
        """

    async def upload_archive(
        self,
        *,
        vaultName: str,
        accountId: str = "-",
        archiveDescription: str = ...,
        checksum: str = ...,
        body: BlobTypeDef = ...,
    ) -> ArchiveCreationOutputTypeDef:
        """
        This operation adds an archive to a vault.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.upload_archive)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#upload_archive)
        """

    async def upload_multipart_part(
        self,
        *,
        vaultName: str,
        uploadId: str,
        accountId: str = "-",
        checksum: str = ...,
        range: str = ...,
        body: BlobTypeDef = ...,
    ) -> UploadMultipartPartOutputTypeDef:
        """
        This operation uploads a part of an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.upload_multipart_part)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#upload_multipart_part)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_jobs"]) -> ListJobsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_multipart_uploads"]
    ) -> ListMultipartUploadsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_parts"]) -> ListPartsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_vaults"]) -> ListVaultsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_paginator)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["vault_exists"]) -> VaultExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_waiter)
        """

    @overload
    def get_waiter(self, waiter_name: Literal["vault_not_exists"]) -> VaultNotExistsWaiter:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.get_waiter)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/#get_waiter)
        """

    async def __aenter__(self) -> "GlacierClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/client/)
        """
