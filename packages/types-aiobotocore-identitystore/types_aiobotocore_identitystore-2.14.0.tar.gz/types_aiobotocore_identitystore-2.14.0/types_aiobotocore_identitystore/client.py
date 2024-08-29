"""
Type annotations for identitystore service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_identitystore.client import IdentityStoreClient

    session = get_session()
    async with session.create_client("identitystore") as client:
        client: IdentityStoreClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListGroupMembershipsForMemberPaginator,
    ListGroupMembershipsPaginator,
    ListGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AddressTypeDef,
    AlternateIdentifierTypeDef,
    AttributeOperationTypeDef,
    CreateGroupMembershipResponseTypeDef,
    CreateGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    DescribeGroupMembershipResponseTypeDef,
    DescribeGroupResponseTypeDef,
    DescribeUserResponseTypeDef,
    EmailTypeDef,
    FilterTypeDef,
    GetGroupIdResponseTypeDef,
    GetGroupMembershipIdResponseTypeDef,
    GetUserIdResponseTypeDef,
    IsMemberInGroupsResponseTypeDef,
    ListGroupMembershipsForMemberResponseTypeDef,
    ListGroupMembershipsResponseTypeDef,
    ListGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    MemberIdTypeDef,
    NameTypeDef,
    PhoneNumberTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("IdentityStoreClient",)


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


class IdentityStoreClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IdentityStoreClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#close)
        """

    async def create_group(
        self, *, IdentityStoreId: str, DisplayName: str = ..., Description: str = ...
    ) -> CreateGroupResponseTypeDef:
        """
        Creates a group within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#create_group)
        """

    async def create_group_membership(
        self, *, IdentityStoreId: str, GroupId: str, MemberId: MemberIdTypeDef
    ) -> CreateGroupMembershipResponseTypeDef:
        """
        Creates a relationship between a member and a group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_group_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#create_group_membership)
        """

    async def create_user(
        self,
        *,
        IdentityStoreId: str,
        UserName: str = ...,
        Name: NameTypeDef = ...,
        DisplayName: str = ...,
        NickName: str = ...,
        ProfileUrl: str = ...,
        Emails: Sequence[EmailTypeDef] = ...,
        Addresses: Sequence[AddressTypeDef] = ...,
        PhoneNumbers: Sequence[PhoneNumberTypeDef] = ...,
        UserType: str = ...,
        Title: str = ...,
        PreferredLanguage: str = ...,
        Locale: str = ...,
        Timezone: str = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user within the specified identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#create_user)
        """

    async def delete_group(self, *, IdentityStoreId: str, GroupId: str) -> Dict[str, Any]:
        """
        Delete a group within an identity store given `GroupId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#delete_group)
        """

    async def delete_group_membership(
        self, *, IdentityStoreId: str, MembershipId: str
    ) -> Dict[str, Any]:
        """
        Delete a membership within a group given `MembershipId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_group_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#delete_group_membership)
        """

    async def delete_user(self, *, IdentityStoreId: str, UserId: str) -> Dict[str, Any]:
        """
        Deletes a user within an identity store given `UserId`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#delete_user)
        """

    async def describe_group(
        self, *, IdentityStoreId: str, GroupId: str
    ) -> DescribeGroupResponseTypeDef:
        """
        Retrieves the group metadata and attributes from `GroupId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#describe_group)
        """

    async def describe_group_membership(
        self, *, IdentityStoreId: str, MembershipId: str
    ) -> DescribeGroupMembershipResponseTypeDef:
        """
        Retrieves membership metadata and attributes from `MembershipId` in an identity
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_group_membership)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#describe_group_membership)
        """

    async def describe_user(
        self, *, IdentityStoreId: str, UserId: str
    ) -> DescribeUserResponseTypeDef:
        """
        Retrieves the user metadata and attributes from the `UserId` in an identity
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.describe_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#describe_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#generate_presigned_url)
        """

    async def get_group_id(
        self, *, IdentityStoreId: str, AlternateIdentifier: AlternateIdentifierTypeDef
    ) -> GetGroupIdResponseTypeDef:
        """
        Retrieves `GroupId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_group_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_group_id)
        """

    async def get_group_membership_id(
        self, *, IdentityStoreId: str, GroupId: str, MemberId: MemberIdTypeDef
    ) -> GetGroupMembershipIdResponseTypeDef:
        """
        Retrieves the `MembershipId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_group_membership_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_group_membership_id)
        """

    async def get_user_id(
        self, *, IdentityStoreId: str, AlternateIdentifier: AlternateIdentifierTypeDef
    ) -> GetUserIdResponseTypeDef:
        """
        Retrieves the `UserId` in an identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_user_id)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_user_id)
        """

    async def is_member_in_groups(
        self, *, IdentityStoreId: str, MemberId: MemberIdTypeDef, GroupIds: Sequence[str]
    ) -> IsMemberInGroupsResponseTypeDef:
        """
        Checks the user's membership in all requested groups and returns if the member
        exists in all queried
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.is_member_in_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#is_member_in_groups)
        """

    async def list_group_memberships(
        self, *, IdentityStoreId: str, GroupId: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGroupMembershipsResponseTypeDef:
        """
        For the specified group in the specified identity store, returns the list of
        all `GroupMembership` objects and returns results in paginated
        form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_group_memberships)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_group_memberships)
        """

    async def list_group_memberships_for_member(
        self,
        *,
        IdentityStoreId: str,
        MemberId: MemberIdTypeDef,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListGroupMembershipsForMemberResponseTypeDef:
        """
        For the specified member in the specified identity store, returns the list of
        all `GroupMembership` objects and returns results in paginated
        form.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_group_memberships_for_member)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_group_memberships_for_member)
        """

    async def list_groups(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ListGroupsResponseTypeDef:
        """
        Lists all groups in the identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_groups)
        """

    async def list_users(
        self,
        *,
        IdentityStoreId: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: Sequence[FilterTypeDef] = ...,
    ) -> ListUsersResponseTypeDef:
        """
        Lists all users in the identity store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#list_users)
        """

    async def update_group(
        self, *, IdentityStoreId: str, GroupId: str, Operations: Sequence[AttributeOperationTypeDef]
    ) -> Dict[str, Any]:
        """
        For the specified group in the specified identity store, updates the group
        metadata and
        attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.update_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#update_group)
        """

    async def update_user(
        self, *, IdentityStoreId: str, UserId: str, Operations: Sequence[AttributeOperationTypeDef]
    ) -> Dict[str, Any]:
        """
        For the specified user in the specified identity store, updates the user
        metadata and
        attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships"]
    ) -> ListGroupMembershipsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_group_memberships_for_member"]
    ) -> ListGroupMembershipsForMemberPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_groups"]) -> ListGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/#get_paginator)
        """

    async def __aenter__(self) -> "IdentityStoreClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/identitystore.html#IdentityStore.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_identitystore/client/)
        """
