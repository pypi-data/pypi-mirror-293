"""
Type annotations for ram service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ram.client import RAMClient

    session = get_session()
    async with session.create_client("ram") as client:
        client: RAMClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    PermissionFeatureSetType,
    PermissionTypeFilterType,
    ReplacePermissionAssociationsWorkStatusType,
    ResourceOwnerType,
    ResourceRegionScopeFilterType,
    ResourceShareAssociationStatusType,
    ResourceShareAssociationTypeType,
    ResourceShareStatusType,
)
from .paginator import (
    GetResourcePoliciesPaginator,
    GetResourceShareAssociationsPaginator,
    GetResourceShareInvitationsPaginator,
    GetResourceSharesPaginator,
    ListPrincipalsPaginator,
    ListResourcesPaginator,
)
from .type_defs import (
    AcceptResourceShareInvitationResponseTypeDef,
    AssociateResourceSharePermissionResponseTypeDef,
    AssociateResourceShareResponseTypeDef,
    CreatePermissionResponseTypeDef,
    CreatePermissionVersionResponseTypeDef,
    CreateResourceShareResponseTypeDef,
    DeletePermissionResponseTypeDef,
    DeletePermissionVersionResponseTypeDef,
    DeleteResourceShareResponseTypeDef,
    DisassociateResourceSharePermissionResponseTypeDef,
    DisassociateResourceShareResponseTypeDef,
    EnableSharingWithAwsOrganizationResponseTypeDef,
    GetPermissionResponseTypeDef,
    GetResourcePoliciesResponseTypeDef,
    GetResourceShareAssociationsResponseTypeDef,
    GetResourceShareInvitationsResponseTypeDef,
    GetResourceSharesResponseTypeDef,
    ListPendingInvitationResourcesResponseTypeDef,
    ListPermissionAssociationsResponseTypeDef,
    ListPermissionsResponseTypeDef,
    ListPermissionVersionsResponseTypeDef,
    ListPrincipalsResponseTypeDef,
    ListReplacePermissionAssociationsWorkResponseTypeDef,
    ListResourceSharePermissionsResponseTypeDef,
    ListResourcesResponseTypeDef,
    ListResourceTypesResponseTypeDef,
    PromotePermissionCreatedFromPolicyResponseTypeDef,
    PromoteResourceShareCreatedFromPolicyResponseTypeDef,
    RejectResourceShareInvitationResponseTypeDef,
    ReplacePermissionAssociationsResponseTypeDef,
    SetDefaultPermissionVersionResponseTypeDef,
    TagFilterTypeDef,
    TagTypeDef,
    UpdateResourceShareResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("RAMClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    IdempotentParameterMismatchException: Type[BotocoreClientError]
    InvalidClientTokenException: Type[BotocoreClientError]
    InvalidMaxResultsException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidPolicyException: Type[BotocoreClientError]
    InvalidResourceTypeException: Type[BotocoreClientError]
    InvalidStateTransitionException: Type[BotocoreClientError]
    MalformedArnException: Type[BotocoreClientError]
    MalformedPolicyTemplateException: Type[BotocoreClientError]
    MissingRequiredParameterException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    PermissionAlreadyExistsException: Type[BotocoreClientError]
    PermissionLimitExceededException: Type[BotocoreClientError]
    PermissionVersionsLimitExceededException: Type[BotocoreClientError]
    ResourceArnNotFoundException: Type[BotocoreClientError]
    ResourceShareInvitationAlreadyAcceptedException: Type[BotocoreClientError]
    ResourceShareInvitationAlreadyRejectedException: Type[BotocoreClientError]
    ResourceShareInvitationArnNotFoundException: Type[BotocoreClientError]
    ResourceShareInvitationExpiredException: Type[BotocoreClientError]
    ResourceShareLimitExceededException: Type[BotocoreClientError]
    ServerInternalException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TagLimitExceededException: Type[BotocoreClientError]
    TagPolicyViolationException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnknownResourceException: Type[BotocoreClientError]
    UnmatchedPolicyPermissionException: Type[BotocoreClientError]


class RAMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RAMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#exceptions)
        """

    async def accept_resource_share_invitation(
        self, *, resourceShareInvitationArn: str, clientToken: str = ...
    ) -> AcceptResourceShareInvitationResponseTypeDef:
        """
        Accepts an invitation to a resource share from another Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.accept_resource_share_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#accept_resource_share_invitation)
        """

    async def associate_resource_share(
        self,
        *,
        resourceShareArn: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        clientToken: str = ...,
        sources: Sequence[str] = ...,
    ) -> AssociateResourceShareResponseTypeDef:
        """
        Adds the specified list of principals and list of resources to a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.associate_resource_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#associate_resource_share)
        """

    async def associate_resource_share_permission(
        self,
        *,
        resourceShareArn: str,
        permissionArn: str,
        replace: bool = ...,
        clientToken: str = ...,
        permissionVersion: int = ...,
    ) -> AssociateResourceSharePermissionResponseTypeDef:
        """
        Adds or replaces the RAM permission for a resource type included in a resource
        share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.associate_resource_share_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#associate_resource_share_permission)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#close)
        """

    async def create_permission(
        self,
        *,
        name: str,
        resourceType: str,
        policyTemplate: str,
        clientToken: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreatePermissionResponseTypeDef:
        """
        Creates a customer managed permission for a specified resource type that you
        can attach to resource
        shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.create_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#create_permission)
        """

    async def create_permission_version(
        self, *, permissionArn: str, policyTemplate: str, clientToken: str = ...
    ) -> CreatePermissionVersionResponseTypeDef:
        """
        Creates a new version of the specified customer managed permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.create_permission_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#create_permission_version)
        """

    async def create_resource_share(
        self,
        *,
        name: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        tags: Sequence[TagTypeDef] = ...,
        allowExternalPrincipals: bool = ...,
        clientToken: str = ...,
        permissionArns: Sequence[str] = ...,
        sources: Sequence[str] = ...,
    ) -> CreateResourceShareResponseTypeDef:
        """
        Creates a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.create_resource_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#create_resource_share)
        """

    async def delete_permission(
        self, *, permissionArn: str, clientToken: str = ...
    ) -> DeletePermissionResponseTypeDef:
        """
        Deletes the specified customer managed permission in the Amazon Web Services
        Region in which you call this
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.delete_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#delete_permission)
        """

    async def delete_permission_version(
        self, *, permissionArn: str, permissionVersion: int, clientToken: str = ...
    ) -> DeletePermissionVersionResponseTypeDef:
        """
        Deletes one version of a customer managed permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.delete_permission_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#delete_permission_version)
        """

    async def delete_resource_share(
        self, *, resourceShareArn: str, clientToken: str = ...
    ) -> DeleteResourceShareResponseTypeDef:
        """
        Deletes the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.delete_resource_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#delete_resource_share)
        """

    async def disassociate_resource_share(
        self,
        *,
        resourceShareArn: str,
        resourceArns: Sequence[str] = ...,
        principals: Sequence[str] = ...,
        clientToken: str = ...,
        sources: Sequence[str] = ...,
    ) -> DisassociateResourceShareResponseTypeDef:
        """
        Removes the specified principals or resources from participating in the
        specified resource
        share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.disassociate_resource_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#disassociate_resource_share)
        """

    async def disassociate_resource_share_permission(
        self, *, resourceShareArn: str, permissionArn: str, clientToken: str = ...
    ) -> DisassociateResourceSharePermissionResponseTypeDef:
        """
        Removes a managed permission from a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.disassociate_resource_share_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#disassociate_resource_share_permission)
        """

    async def enable_sharing_with_aws_organization(
        self,
    ) -> EnableSharingWithAwsOrganizationResponseTypeDef:
        """
        Enables resource sharing within your organization in Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.enable_sharing_with_aws_organization)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#enable_sharing_with_aws_organization)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#generate_presigned_url)
        """

    async def get_permission(
        self, *, permissionArn: str, permissionVersion: int = ...
    ) -> GetPermissionResponseTypeDef:
        """
        Retrieves the contents of a managed permission in JSON format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_permission)
        """

    async def get_resource_policies(
        self,
        *,
        resourceArns: Sequence[str],
        principal: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetResourcePoliciesResponseTypeDef:
        """
        Retrieves the resource policies for the specified resources that you own and
        have
        shared.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_resource_policies)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_resource_policies)
        """

    async def get_resource_share_associations(
        self,
        *,
        associationType: ResourceShareAssociationTypeType,
        resourceShareArns: Sequence[str] = ...,
        resourceArn: str = ...,
        principal: str = ...,
        associationStatus: ResourceShareAssociationStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetResourceShareAssociationsResponseTypeDef:
        """
        Retrieves the lists of resources and principals that associated for resource
        shares that you
        own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_resource_share_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_resource_share_associations)
        """

    async def get_resource_share_invitations(
        self,
        *,
        resourceShareInvitationArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> GetResourceShareInvitationsResponseTypeDef:
        """
        Retrieves details about invitations that you have received for resource shares.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_resource_share_invitations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_resource_share_invitations)
        """

    async def get_resource_shares(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceShareArns: Sequence[str] = ...,
        resourceShareStatus: ResourceShareStatusType = ...,
        name: str = ...,
        tagFilters: Sequence[TagFilterTypeDef] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        permissionArn: str = ...,
        permissionVersion: int = ...,
    ) -> GetResourceSharesResponseTypeDef:
        """
        Retrieves details about the resource shares that you own or that are shared
        with
        you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_resource_shares)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_resource_shares)
        """

    async def list_pending_invitation_resources(
        self,
        *,
        resourceShareInvitationArn: str,
        nextToken: str = ...,
        maxResults: int = ...,
        resourceRegionScope: ResourceRegionScopeFilterType = ...,
    ) -> ListPendingInvitationResourcesResponseTypeDef:
        """
        Lists the resources in a resource share that is shared with you but for which
        the invitation is still
        `PENDING`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_pending_invitation_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_pending_invitation_resources)
        """

    async def list_permission_associations(
        self,
        *,
        permissionArn: str = ...,
        permissionVersion: int = ...,
        associationStatus: ResourceShareAssociationStatusType = ...,
        resourceType: str = ...,
        featureSet: PermissionFeatureSetType = ...,
        defaultVersion: bool = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListPermissionAssociationsResponseTypeDef:
        """
        Lists information about the managed permission and its associations to any
        resource shares that use this managed
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_permission_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_permission_associations)
        """

    async def list_permission_versions(
        self, *, permissionArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListPermissionVersionsResponseTypeDef:
        """
        Lists the available versions of the specified RAM permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_permission_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_permission_versions)
        """

    async def list_permissions(
        self,
        *,
        resourceType: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        permissionType: PermissionTypeFilterType = ...,
    ) -> ListPermissionsResponseTypeDef:
        """
        Retrieves a list of available RAM permissions that you can use for the
        supported resource
        types.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_permissions)
        """

    async def list_principals(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        resourceArn: str = ...,
        principals: Sequence[str] = ...,
        resourceType: str = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListPrincipalsResponseTypeDef:
        """
        Lists the principals that you are sharing resources with or that are sharing
        resources with
        you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_principals)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_principals)
        """

    async def list_replace_permission_associations_work(
        self,
        *,
        workIds: Sequence[str] = ...,
        status: ReplacePermissionAssociationsWorkStatusType = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListReplacePermissionAssociationsWorkResponseTypeDef:
        """
        Retrieves the current status of the asynchronous tasks performed by RAM when
        you perform the  ReplacePermissionAssociationsWork
        operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_replace_permission_associations_work)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_replace_permission_associations_work)
        """

    async def list_resource_share_permissions(
        self, *, resourceShareArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListResourceSharePermissionsResponseTypeDef:
        """
        Lists the RAM permissions that are associated with a resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_resource_share_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_resource_share_permissions)
        """

    async def list_resource_types(
        self,
        *,
        nextToken: str = ...,
        maxResults: int = ...,
        resourceRegionScope: ResourceRegionScopeFilterType = ...,
    ) -> ListResourceTypesResponseTypeDef:
        """
        Lists the resource types that can be shared by RAM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_resource_types)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_resource_types)
        """

    async def list_resources(
        self,
        *,
        resourceOwner: ResourceOwnerType,
        principal: str = ...,
        resourceType: str = ...,
        resourceArns: Sequence[str] = ...,
        resourceShareArns: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
        resourceRegionScope: ResourceRegionScopeFilterType = ...,
    ) -> ListResourcesResponseTypeDef:
        """
        Lists the resources that you added to a resource share or the resources that
        are shared with
        you.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.list_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#list_resources)
        """

    async def promote_permission_created_from_policy(
        self, *, permissionArn: str, name: str, clientToken: str = ...
    ) -> PromotePermissionCreatedFromPolicyResponseTypeDef:
        """
        When you attach a resource-based policy to a resource, RAM automatically
        creates a resource share of `featureSet`= `CREATED_FROM_POLICY` with a managed
        permission that has the same IAM permissions as the original resource-based
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.promote_permission_created_from_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#promote_permission_created_from_policy)
        """

    async def promote_resource_share_created_from_policy(
        self, *, resourceShareArn: str
    ) -> PromoteResourceShareCreatedFromPolicyResponseTypeDef:
        """
        When you attach a resource-based policy to a resource, RAM automatically
        creates a resource share of `featureSet`= `CREATED_FROM_POLICY` with a managed
        permission that has the same IAM permissions as the original resource-based
        policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.promote_resource_share_created_from_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#promote_resource_share_created_from_policy)
        """

    async def reject_resource_share_invitation(
        self, *, resourceShareInvitationArn: str, clientToken: str = ...
    ) -> RejectResourceShareInvitationResponseTypeDef:
        """
        Rejects an invitation to a resource share from another Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.reject_resource_share_invitation)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#reject_resource_share_invitation)
        """

    async def replace_permission_associations(
        self,
        *,
        fromPermissionArn: str,
        toPermissionArn: str,
        fromPermissionVersion: int = ...,
        clientToken: str = ...,
    ) -> ReplacePermissionAssociationsResponseTypeDef:
        """
        Updates all resource shares that use a managed permission to a different
        managed
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.replace_permission_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#replace_permission_associations)
        """

    async def set_default_permission_version(
        self, *, permissionArn: str, permissionVersion: int, clientToken: str = ...
    ) -> SetDefaultPermissionVersionResponseTypeDef:
        """
        Designates the specified version number as the default version for the
        specified customer managed
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.set_default_permission_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#set_default_permission_version)
        """

    async def tag_resource(
        self, *, tags: Sequence[TagTypeDef], resourceShareArn: str = ..., resourceArn: str = ...
    ) -> Dict[str, Any]:
        """
        Adds the specified tag keys and values to a resource share or managed
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#tag_resource)
        """

    async def untag_resource(
        self, *, tagKeys: Sequence[str], resourceShareArn: str = ..., resourceArn: str = ...
    ) -> Dict[str, Any]:
        """
        Removes the specified tag key and value pairs from the specified resource share
        or managed
        permission.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#untag_resource)
        """

    async def update_resource_share(
        self,
        *,
        resourceShareArn: str,
        name: str = ...,
        allowExternalPrincipals: bool = ...,
        clientToken: str = ...,
    ) -> UpdateResourceShareResponseTypeDef:
        """
        Modifies some of the properties of the specified resource share.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.update_resource_share)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#update_resource_share)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_share_associations"]
    ) -> GetResourceShareAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_share_invitations"]
    ) -> GetResourceShareInvitationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_resource_shares"]
    ) -> GetResourceSharesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_principals"]) -> ListPrincipalsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/#get_paginator)
        """

    async def __aenter__(self) -> "RAMClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ram.html#RAM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ram/client/)
        """
