"""
Type annotations for s3control service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_s3control.client import S3ControlClient

    session = get_session()
    async with session.create_client("s3control") as client:
        client: S3ControlClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BucketCannedACLType,
    GranteeTypeType,
    JobStatusType,
    PermissionType,
    PrivilegeType,
    RequestedJobStatusType,
)
from .paginator import ListAccessPointsForObjectLambdaPaginator
from .type_defs import (
    AccessGrantsLocationConfigurationTypeDef,
    CreateAccessGrantResultTypeDef,
    CreateAccessGrantsInstanceResultTypeDef,
    CreateAccessGrantsLocationResultTypeDef,
    CreateAccessPointForObjectLambdaResultTypeDef,
    CreateAccessPointResultTypeDef,
    CreateBucketConfigurationTypeDef,
    CreateBucketResultTypeDef,
    CreateJobResultTypeDef,
    CreateMultiRegionAccessPointInputUnionTypeDef,
    CreateMultiRegionAccessPointResultTypeDef,
    DeleteMultiRegionAccessPointInputTypeDef,
    DeleteMultiRegionAccessPointResultTypeDef,
    DescribeJobResultTypeDef,
    DescribeMultiRegionAccessPointOperationResultTypeDef,
    EmptyResponseMetadataTypeDef,
    GetAccessGrantResultTypeDef,
    GetAccessGrantsInstanceForPrefixResultTypeDef,
    GetAccessGrantsInstanceResourcePolicyResultTypeDef,
    GetAccessGrantsInstanceResultTypeDef,
    GetAccessGrantsLocationResultTypeDef,
    GetAccessPointConfigurationForObjectLambdaResultTypeDef,
    GetAccessPointForObjectLambdaResultTypeDef,
    GetAccessPointPolicyForObjectLambdaResultTypeDef,
    GetAccessPointPolicyResultTypeDef,
    GetAccessPointPolicyStatusForObjectLambdaResultTypeDef,
    GetAccessPointPolicyStatusResultTypeDef,
    GetAccessPointResultTypeDef,
    GetBucketLifecycleConfigurationResultTypeDef,
    GetBucketPolicyResultTypeDef,
    GetBucketReplicationResultTypeDef,
    GetBucketResultTypeDef,
    GetBucketTaggingResultTypeDef,
    GetBucketVersioningResultTypeDef,
    GetDataAccessResultTypeDef,
    GetJobTaggingResultTypeDef,
    GetMultiRegionAccessPointPolicyResultTypeDef,
    GetMultiRegionAccessPointPolicyStatusResultTypeDef,
    GetMultiRegionAccessPointResultTypeDef,
    GetMultiRegionAccessPointRoutesResultTypeDef,
    GetPublicAccessBlockOutputTypeDef,
    GetStorageLensConfigurationResultTypeDef,
    GetStorageLensConfigurationTaggingResultTypeDef,
    GetStorageLensGroupResultTypeDef,
    GranteeTypeDef,
    JobManifestGeneratorUnionTypeDef,
    JobManifestUnionTypeDef,
    JobOperationUnionTypeDef,
    JobReportTypeDef,
    LifecycleConfigurationTypeDef,
    ListAccessGrantsInstancesResultTypeDef,
    ListAccessGrantsLocationsResultTypeDef,
    ListAccessGrantsResultTypeDef,
    ListAccessPointsForObjectLambdaResultTypeDef,
    ListAccessPointsResultTypeDef,
    ListJobsResultTypeDef,
    ListMultiRegionAccessPointsResultTypeDef,
    ListRegionalBucketsResultTypeDef,
    ListStorageLensConfigurationsResultTypeDef,
    ListStorageLensGroupsResultTypeDef,
    ListTagsForResourceResultTypeDef,
    MultiRegionAccessPointRouteTypeDef,
    ObjectLambdaConfigurationUnionTypeDef,
    PublicAccessBlockConfigurationTypeDef,
    PutAccessGrantsInstanceResourcePolicyResultTypeDef,
    PutMultiRegionAccessPointPolicyInputTypeDef,
    PutMultiRegionAccessPointPolicyResultTypeDef,
    ReplicationConfigurationUnionTypeDef,
    S3TagTypeDef,
    StorageLensConfigurationUnionTypeDef,
    StorageLensGroupUnionTypeDef,
    StorageLensTagTypeDef,
    TaggingTypeDef,
    TagTypeDef,
    UpdateAccessGrantsLocationResultTypeDef,
    UpdateJobPriorityResultTypeDef,
    UpdateJobStatusResultTypeDef,
    VersioningConfigurationTypeDef,
    VpcConfigurationTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("S3ControlClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    BadRequestException: Type[BotocoreClientError]
    BucketAlreadyExists: Type[BotocoreClientError]
    BucketAlreadyOwnedByYou: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    IdempotencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    JobStatusException: Type[BotocoreClientError]
    NoSuchPublicAccessBlockConfiguration: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]

class S3ControlClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3ControlClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#exceptions)
        """

    async def associate_access_grants_identity_center(
        self, *, AccountId: str, IdentityCenterArn: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associate your S3 Access Grants instance with an Amazon Web Services IAM
        Identity Center
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.associate_access_grants_identity_center)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#associate_access_grants_identity_center)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#close)
        """

    async def create_access_grant(
        self,
        *,
        AccountId: str,
        AccessGrantsLocationId: str,
        Grantee: GranteeTypeDef,
        Permission: PermissionType,
        AccessGrantsLocationConfiguration: AccessGrantsLocationConfigurationTypeDef = ...,
        ApplicationArn: str = ...,
        S3PrefixType: Literal["Object"] = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateAccessGrantResultTypeDef:
        """
        Creates an access grant that gives a grantee access to your S3 data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_access_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_access_grant)
        """

    async def create_access_grants_instance(
        self, *, AccountId: str, IdentityCenterArn: str = ..., Tags: Sequence[TagTypeDef] = ...
    ) -> CreateAccessGrantsInstanceResultTypeDef:
        """
        Creates an S3 Access Grants instance, which serves as a logical grouping for
        access
        grants.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_access_grants_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_access_grants_instance)
        """

    async def create_access_grants_location(
        self,
        *,
        AccountId: str,
        LocationScope: str,
        IAMRoleArn: str,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateAccessGrantsLocationResultTypeDef:
        """
        The S3 data location that you would like to register in your S3 Access Grants
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_access_grants_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_access_grants_location)
        """

    async def create_access_point(
        self,
        *,
        AccountId: str,
        Name: str,
        Bucket: str,
        VpcConfiguration: VpcConfigurationTypeDef = ...,
        PublicAccessBlockConfiguration: PublicAccessBlockConfigurationTypeDef = ...,
        BucketAccountId: str = ...,
    ) -> CreateAccessPointResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_access_point)
        """

    async def create_access_point_for_object_lambda(
        self, *, AccountId: str, Name: str, Configuration: ObjectLambdaConfigurationUnionTypeDef
    ) -> CreateAccessPointForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_access_point_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_access_point_for_object_lambda)
        """

    async def create_bucket(
        self,
        *,
        Bucket: str,
        ACL: BucketCannedACLType = ...,
        CreateBucketConfiguration: CreateBucketConfigurationTypeDef = ...,
        GrantFullControl: str = ...,
        GrantRead: str = ...,
        GrantReadACP: str = ...,
        GrantWrite: str = ...,
        GrantWriteACP: str = ...,
        ObjectLockEnabledForBucket: bool = ...,
        OutpostId: str = ...,
    ) -> CreateBucketResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_bucket)
        """

    async def create_job(
        self,
        *,
        AccountId: str,
        Operation: JobOperationUnionTypeDef,
        Report: JobReportTypeDef,
        ClientRequestToken: str,
        Priority: int,
        RoleArn: str,
        ConfirmationRequired: bool = ...,
        Manifest: JobManifestUnionTypeDef = ...,
        Description: str = ...,
        Tags: Sequence[S3TagTypeDef] = ...,
        ManifestGenerator: JobManifestGeneratorUnionTypeDef = ...,
    ) -> CreateJobResultTypeDef:
        """
        This operation creates an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_job)
        """

    async def create_multi_region_access_point(
        self,
        *,
        AccountId: str,
        ClientToken: str,
        Details: CreateMultiRegionAccessPointInputUnionTypeDef,
    ) -> CreateMultiRegionAccessPointResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_multi_region_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_multi_region_access_point)
        """

    async def create_storage_lens_group(
        self,
        *,
        AccountId: str,
        StorageLensGroup: StorageLensGroupUnionTypeDef,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new S3 Storage Lens group and associates it with the specified Amazon
        Web Services account
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.create_storage_lens_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#create_storage_lens_group)
        """

    async def delete_access_grant(
        self, *, AccountId: str, AccessGrantId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the access grant from the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_grant)
        """

    async def delete_access_grants_instance(
        self, *, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_grants_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_grants_instance)
        """

    async def delete_access_grants_instance_resource_policy(
        self, *, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_grants_instance_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_grants_instance_resource_policy)
        """

    async def delete_access_grants_location(
        self, *, AccountId: str, AccessGrantsLocationId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deregisters a location from your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_grants_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_grants_location)
        """

    async def delete_access_point(
        self, *, AccountId: str, Name: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_point)
        """

    async def delete_access_point_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_point_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_point_for_object_lambda)
        """

    async def delete_access_point_policy(
        self, *, AccountId: str, Name: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_point_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_point_policy)
        """

    async def delete_access_point_policy_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_access_point_policy_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_access_point_policy_for_object_lambda)
        """

    async def delete_bucket(self, *, AccountId: str, Bucket: str) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_bucket)
        """

    async def delete_bucket_lifecycle_configuration(
        self, *, AccountId: str, Bucket: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_bucket_lifecycle_configuration)
        """

    async def delete_bucket_policy(
        self, *, AccountId: str, Bucket: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_bucket_policy)
        """

    async def delete_bucket_replication(
        self, *, AccountId: str, Bucket: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_bucket_replication)
        """

    async def delete_bucket_tagging(
        self, *, AccountId: str, Bucket: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_bucket_tagging)
        """

    async def delete_job_tagging(self, *, AccountId: str, JobId: str) -> Dict[str, Any]:
        """
        Removes the entire tag set from the specified S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_job_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_job_tagging)
        """

    async def delete_multi_region_access_point(
        self, *, AccountId: str, ClientToken: str, Details: DeleteMultiRegionAccessPointInputTypeDef
    ) -> DeleteMultiRegionAccessPointResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_multi_region_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_multi_region_access_point)
        """

    async def delete_public_access_block(self, *, AccountId: str) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_public_access_block)
        """

    async def delete_storage_lens_configuration(
        self, *, ConfigId: str, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_storage_lens_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_storage_lens_configuration)
        """

    async def delete_storage_lens_configuration_tagging(
        self, *, ConfigId: str, AccountId: str
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_storage_lens_configuration_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_storage_lens_configuration_tagging)
        """

    async def delete_storage_lens_group(
        self, *, Name: str, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an existing S3 Storage Lens group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.delete_storage_lens_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#delete_storage_lens_group)
        """

    async def describe_job(self, *, AccountId: str, JobId: str) -> DescribeJobResultTypeDef:
        """
        Retrieves the configuration parameters and status for a Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.describe_job)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#describe_job)
        """

    async def describe_multi_region_access_point_operation(
        self, *, AccountId: str, RequestTokenARN: str
    ) -> DescribeMultiRegionAccessPointOperationResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.describe_multi_region_access_point_operation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#describe_multi_region_access_point_operation)
        """

    async def dissociate_access_grants_identity_center(
        self, *, AccountId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Dissociates the Amazon Web Services IAM Identity Center instance from the S3
        Access Grants
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.dissociate_access_grants_identity_center)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#dissociate_access_grants_identity_center)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#generate_presigned_url)
        """

    async def get_access_grant(
        self, *, AccountId: str, AccessGrantId: str
    ) -> GetAccessGrantResultTypeDef:
        """
        Get the details of an access grant from your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_grant)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_grant)
        """

    async def get_access_grants_instance(
        self, *, AccountId: str
    ) -> GetAccessGrantsInstanceResultTypeDef:
        """
        Retrieves the S3 Access Grants instance for a Region in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_grants_instance)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_grants_instance)
        """

    async def get_access_grants_instance_for_prefix(
        self, *, AccountId: str, S3Prefix: str
    ) -> GetAccessGrantsInstanceForPrefixResultTypeDef:
        """
        Retrieve the S3 Access Grants instance that contains a particular prefix.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_grants_instance_for_prefix)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_grants_instance_for_prefix)
        """

    async def get_access_grants_instance_resource_policy(
        self, *, AccountId: str
    ) -> GetAccessGrantsInstanceResourcePolicyResultTypeDef:
        """
        Returns the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_grants_instance_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_grants_instance_resource_policy)
        """

    async def get_access_grants_location(
        self, *, AccountId: str, AccessGrantsLocationId: str
    ) -> GetAccessGrantsLocationResultTypeDef:
        """
        Retrieves the details of a particular location registered in your S3 Access
        Grants
        instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_grants_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_grants_location)
        """

    async def get_access_point(self, *, AccountId: str, Name: str) -> GetAccessPointResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point)
        """

    async def get_access_point_configuration_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointConfigurationForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_configuration_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_configuration_for_object_lambda)
        """

    async def get_access_point_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_for_object_lambda)
        """

    async def get_access_point_policy(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointPolicyResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_policy)
        """

    async def get_access_point_policy_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointPolicyForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_policy_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_policy_for_object_lambda)
        """

    async def get_access_point_policy_status(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointPolicyStatusResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_policy_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_policy_status)
        """

    async def get_access_point_policy_status_for_object_lambda(
        self, *, AccountId: str, Name: str
    ) -> GetAccessPointPolicyStatusForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_access_point_policy_status_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_access_point_policy_status_for_object_lambda)
        """

    async def get_bucket(self, *, AccountId: str, Bucket: str) -> GetBucketResultTypeDef:
        """
        Gets an Amazon S3 on Outposts bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket)
        """

    async def get_bucket_lifecycle_configuration(
        self, *, AccountId: str, Bucket: str
    ) -> GetBucketLifecycleConfigurationResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket_lifecycle_configuration)
        """

    async def get_bucket_policy(
        self, *, AccountId: str, Bucket: str
    ) -> GetBucketPolicyResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket_policy)
        """

    async def get_bucket_replication(
        self, *, AccountId: str, Bucket: str
    ) -> GetBucketReplicationResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket_replication)
        """

    async def get_bucket_tagging(
        self, *, AccountId: str, Bucket: str
    ) -> GetBucketTaggingResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket_tagging)
        """

    async def get_bucket_versioning(
        self, *, AccountId: str, Bucket: str
    ) -> GetBucketVersioningResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_bucket_versioning)
        """

    async def get_data_access(
        self,
        *,
        AccountId: str,
        Target: str,
        Permission: PermissionType,
        DurationSeconds: int = ...,
        Privilege: PrivilegeType = ...,
        TargetType: Literal["Object"] = ...,
    ) -> GetDataAccessResultTypeDef:
        """
        Returns a temporary access credential from S3 Access Grants to the grantee or
        client
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_data_access)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_data_access)
        """

    async def get_job_tagging(self, *, AccountId: str, JobId: str) -> GetJobTaggingResultTypeDef:
        """
        Returns the tags on an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_job_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_job_tagging)
        """

    async def get_multi_region_access_point(
        self, *, AccountId: str, Name: str
    ) -> GetMultiRegionAccessPointResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_multi_region_access_point)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_multi_region_access_point)
        """

    async def get_multi_region_access_point_policy(
        self, *, AccountId: str, Name: str
    ) -> GetMultiRegionAccessPointPolicyResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_multi_region_access_point_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_multi_region_access_point_policy)
        """

    async def get_multi_region_access_point_policy_status(
        self, *, AccountId: str, Name: str
    ) -> GetMultiRegionAccessPointPolicyStatusResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_multi_region_access_point_policy_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_multi_region_access_point_policy_status)
        """

    async def get_multi_region_access_point_routes(
        self, *, AccountId: str, Mrap: str
    ) -> GetMultiRegionAccessPointRoutesResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_multi_region_access_point_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_multi_region_access_point_routes)
        """

    async def get_public_access_block(self, *, AccountId: str) -> GetPublicAccessBlockOutputTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_public_access_block)
        """

    async def get_storage_lens_configuration(
        self, *, ConfigId: str, AccountId: str
    ) -> GetStorageLensConfigurationResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_storage_lens_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_storage_lens_configuration)
        """

    async def get_storage_lens_configuration_tagging(
        self, *, ConfigId: str, AccountId: str
    ) -> GetStorageLensConfigurationTaggingResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_storage_lens_configuration_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_storage_lens_configuration_tagging)
        """

    async def get_storage_lens_group(
        self, *, Name: str, AccountId: str
    ) -> GetStorageLensGroupResultTypeDef:
        """
        Retrieves the Storage Lens group configuration details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_storage_lens_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_storage_lens_group)
        """

    async def list_access_grants(
        self,
        *,
        AccountId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        GranteeType: GranteeTypeType = ...,
        GranteeIdentifier: str = ...,
        Permission: PermissionType = ...,
        GrantScope: str = ...,
        ApplicationArn: str = ...,
    ) -> ListAccessGrantsResultTypeDef:
        """
        Returns the list of access grants in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_access_grants)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_access_grants)
        """

    async def list_access_grants_instances(
        self, *, AccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccessGrantsInstancesResultTypeDef:
        """
        Returns a list of S3 Access Grants instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_access_grants_instances)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_access_grants_instances)
        """

    async def list_access_grants_locations(
        self,
        *,
        AccountId: str,
        NextToken: str = ...,
        MaxResults: int = ...,
        LocationScope: str = ...,
    ) -> ListAccessGrantsLocationsResultTypeDef:
        """
        Returns a list of the locations registered in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_access_grants_locations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_access_grants_locations)
        """

    async def list_access_points(
        self, *, AccountId: str, Bucket: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccessPointsResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_access_points)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_access_points)
        """

    async def list_access_points_for_object_lambda(
        self, *, AccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListAccessPointsForObjectLambdaResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_access_points_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_access_points_for_object_lambda)
        """

    async def list_jobs(
        self,
        *,
        AccountId: str,
        JobStatuses: Sequence[JobStatusType] = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ListJobsResultTypeDef:
        """
        Lists current S3 Batch Operations jobs as well as the jobs that have ended
        within the last 90 days for the Amazon Web Services account making the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_jobs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_jobs)
        """

    async def list_multi_region_access_points(
        self, *, AccountId: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListMultiRegionAccessPointsResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_multi_region_access_points)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_multi_region_access_points)
        """

    async def list_regional_buckets(
        self, *, AccountId: str, NextToken: str = ..., MaxResults: int = ..., OutpostId: str = ...
    ) -> ListRegionalBucketsResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_regional_buckets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_regional_buckets)
        """

    async def list_storage_lens_configurations(
        self, *, AccountId: str, NextToken: str = ...
    ) -> ListStorageLensConfigurationsResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_storage_lens_configurations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_storage_lens_configurations)
        """

    async def list_storage_lens_groups(
        self, *, AccountId: str, NextToken: str = ...
    ) -> ListStorageLensGroupsResultTypeDef:
        """
        Lists all the Storage Lens groups in the specified home Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_storage_lens_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_storage_lens_groups)
        """

    async def list_tags_for_resource(
        self, *, AccountId: str, ResourceArn: str
    ) -> ListTagsForResourceResultTypeDef:
        """
        This operation allows you to list all the Amazon Web Services resource tags for
        a specified
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#list_tags_for_resource)
        """

    async def put_access_grants_instance_resource_policy(
        self, *, AccountId: str, Policy: str, Organization: str = ...
    ) -> PutAccessGrantsInstanceResourcePolicyResultTypeDef:
        """
        Updates the resource policy of the S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_access_grants_instance_resource_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_access_grants_instance_resource_policy)
        """

    async def put_access_point_configuration_for_object_lambda(
        self, *, AccountId: str, Name: str, Configuration: ObjectLambdaConfigurationUnionTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_access_point_configuration_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_access_point_configuration_for_object_lambda)
        """

    async def put_access_point_policy(
        self, *, AccountId: str, Name: str, Policy: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_access_point_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_access_point_policy)
        """

    async def put_access_point_policy_for_object_lambda(
        self, *, AccountId: str, Name: str, Policy: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_access_point_policy_for_object_lambda)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_access_point_policy_for_object_lambda)
        """

    async def put_bucket_lifecycle_configuration(
        self,
        *,
        AccountId: str,
        Bucket: str,
        LifecycleConfiguration: LifecycleConfigurationTypeDef = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_bucket_lifecycle_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_bucket_lifecycle_configuration)
        """

    async def put_bucket_policy(
        self, *, AccountId: str, Bucket: str, Policy: str, ConfirmRemoveSelfBucketAccess: bool = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_bucket_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_bucket_policy)
        """

    async def put_bucket_replication(
        self,
        *,
        AccountId: str,
        Bucket: str,
        ReplicationConfiguration: ReplicationConfigurationUnionTypeDef,
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_bucket_replication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_bucket_replication)
        """

    async def put_bucket_tagging(
        self, *, AccountId: str, Bucket: str, Tagging: TaggingTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_bucket_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_bucket_tagging)
        """

    async def put_bucket_versioning(
        self,
        *,
        AccountId: str,
        Bucket: str,
        VersioningConfiguration: VersioningConfigurationTypeDef,
        MFA: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_bucket_versioning)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_bucket_versioning)
        """

    async def put_job_tagging(
        self, *, AccountId: str, JobId: str, Tags: Sequence[S3TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Sets the supplied tag-set on an S3 Batch Operations job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_job_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_job_tagging)
        """

    async def put_multi_region_access_point_policy(
        self,
        *,
        AccountId: str,
        ClientToken: str,
        Details: PutMultiRegionAccessPointPolicyInputTypeDef,
    ) -> PutMultiRegionAccessPointPolicyResultTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_multi_region_access_point_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_multi_region_access_point_policy)
        """

    async def put_public_access_block(
        self,
        *,
        PublicAccessBlockConfiguration: PublicAccessBlockConfigurationTypeDef,
        AccountId: str,
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_public_access_block)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_public_access_block)
        """

    async def put_storage_lens_configuration(
        self,
        *,
        ConfigId: str,
        AccountId: str,
        StorageLensConfiguration: StorageLensConfigurationUnionTypeDef,
        Tags: Sequence[StorageLensTagTypeDef] = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_storage_lens_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_storage_lens_configuration)
        """

    async def put_storage_lens_configuration_tagging(
        self, *, ConfigId: str, AccountId: str, Tags: Sequence[StorageLensTagTypeDef]
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.put_storage_lens_configuration_tagging)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#put_storage_lens_configuration_tagging)
        """

    async def submit_multi_region_access_point_routes(
        self,
        *,
        AccountId: str,
        Mrap: str,
        RouteUpdates: Sequence[MultiRegionAccessPointRouteTypeDef],
    ) -> Dict[str, Any]:
        """
        .

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.submit_multi_region_access_point_routes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#submit_multi_region_access_point_routes)
        """

    async def tag_resource(
        self, *, AccountId: str, ResourceArn: str, Tags: Sequence[TagTypeDef]
    ) -> Dict[str, Any]:
        """
        Creates a new Amazon Web Services resource tag or updates an existing resource
        tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#tag_resource)
        """

    async def untag_resource(
        self, *, AccountId: str, ResourceArn: str, TagKeys: Sequence[str]
    ) -> Dict[str, Any]:
        """
        This operation removes the specified Amazon Web Services resource tags from an
        S3
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#untag_resource)
        """

    async def update_access_grants_location(
        self, *, AccountId: str, AccessGrantsLocationId: str, IAMRoleArn: str
    ) -> UpdateAccessGrantsLocationResultTypeDef:
        """
        Updates the IAM role of a registered location in your S3 Access Grants instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.update_access_grants_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#update_access_grants_location)
        """

    async def update_job_priority(
        self, *, AccountId: str, JobId: str, Priority: int
    ) -> UpdateJobPriorityResultTypeDef:
        """
        Updates an existing S3 Batch Operations job's priority.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.update_job_priority)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#update_job_priority)
        """

    async def update_job_status(
        self,
        *,
        AccountId: str,
        JobId: str,
        RequestedJobStatus: RequestedJobStatusType,
        StatusUpdateReason: str = ...,
    ) -> UpdateJobStatusResultTypeDef:
        """
        Updates the status for the specified job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.update_job_status)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#update_job_status)
        """

    async def update_storage_lens_group(
        self, *, Name: str, AccountId: str, StorageLensGroup: StorageLensGroupUnionTypeDef
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the existing Storage Lens group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.update_storage_lens_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#update_storage_lens_group)
        """

    def get_paginator(
        self, operation_name: Literal["list_access_points_for_object_lambda"]
    ) -> ListAccessPointsForObjectLambdaPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/#get_paginator)
        """

    async def __aenter__(self) -> "S3ControlClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_s3control/client/)
        """
