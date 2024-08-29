"""
Type annotations for workdocs service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workdocs.client import WorkDocsClient

    session = get_session()
    async with session.create_client("workdocs") as client:
        client: WorkDocsClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BooleanEnumTypeType,
    CommentVisibilityTypeType,
    FolderContentTypeType,
    LocaleTypeType,
    OrderTypeType,
    PrincipalTypeType,
    ResourceSortTypeType,
    ResourceStateTypeType,
    SearchQueryScopeTypeType,
    SubscriptionProtocolTypeType,
    UserFilterTypeType,
    UserSortTypeType,
    UserTypeType,
)
from .paginator import (
    DescribeActivitiesPaginator,
    DescribeCommentsPaginator,
    DescribeDocumentVersionsPaginator,
    DescribeFolderContentsPaginator,
    DescribeGroupsPaginator,
    DescribeNotificationSubscriptionsPaginator,
    DescribeResourcePermissionsPaginator,
    DescribeRootFoldersPaginator,
    DescribeUsersPaginator,
    SearchResourcesPaginator,
)
from .type_defs import (
    ActivateUserResponseTypeDef,
    AddResourcePermissionsResponseTypeDef,
    CreateCommentResponseTypeDef,
    CreateFolderResponseTypeDef,
    CreateNotificationSubscriptionResponseTypeDef,
    CreateUserResponseTypeDef,
    DescribeActivitiesResponseTypeDef,
    DescribeCommentsResponseTypeDef,
    DescribeDocumentVersionsResponseTypeDef,
    DescribeFolderContentsResponseTypeDef,
    DescribeGroupsResponseTypeDef,
    DescribeNotificationSubscriptionsResponseTypeDef,
    DescribeResourcePermissionsResponseTypeDef,
    DescribeRootFoldersResponseTypeDef,
    DescribeUsersResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    FiltersTypeDef,
    GetCurrentUserResponseTypeDef,
    GetDocumentPathResponseTypeDef,
    GetDocumentResponseTypeDef,
    GetDocumentVersionResponseTypeDef,
    GetFolderPathResponseTypeDef,
    GetFolderResponseTypeDef,
    GetResourcesResponseTypeDef,
    InitiateDocumentVersionUploadResponseTypeDef,
    NotificationOptionsTypeDef,
    SearchResourcesResponseTypeDef,
    SearchSortResultTypeDef,
    SharePrincipalTypeDef,
    StorageRuleTypeTypeDef,
    TimestampTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("WorkDocsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    ConflictingOperationException: Type[BotocoreClientError]
    CustomMetadataLimitExceededException: Type[BotocoreClientError]
    DeactivatingLastSystemUserException: Type[BotocoreClientError]
    DocumentLockedForCommentsException: Type[BotocoreClientError]
    DraftUploadOutOfSyncException: Type[BotocoreClientError]
    EntityAlreadyExistsException: Type[BotocoreClientError]
    EntityNotExistsException: Type[BotocoreClientError]
    FailedDependencyException: Type[BotocoreClientError]
    IllegalUserStateException: Type[BotocoreClientError]
    InvalidArgumentException: Type[BotocoreClientError]
    InvalidCommentOperationException: Type[BotocoreClientError]
    InvalidOperationException: Type[BotocoreClientError]
    InvalidPasswordException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProhibitedStateException: Type[BotocoreClientError]
    RequestedEntityTooLargeException: Type[BotocoreClientError]
    ResourceAlreadyCheckedOutException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    StorageLimitExceededException: Type[BotocoreClientError]
    StorageLimitWillExceedException: Type[BotocoreClientError]
    TooManyLabelsException: Type[BotocoreClientError]
    TooManySubscriptionsException: Type[BotocoreClientError]
    UnauthorizedOperationException: Type[BotocoreClientError]
    UnauthorizedResourceAccessException: Type[BotocoreClientError]


class WorkDocsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkDocsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#exceptions)
        """

    async def abort_document_version_upload(
        self, *, DocumentId: str, VersionId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Aborts the upload of the specified document version that was previously
        initiated by
        InitiateDocumentVersionUpload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.abort_document_version_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#abort_document_version_upload)
        """

    async def activate_user(
        self, *, UserId: str, AuthenticationToken: str = ...
    ) -> ActivateUserResponseTypeDef:
        """
        Activates the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.activate_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#activate_user)
        """

    async def add_resource_permissions(
        self,
        *,
        ResourceId: str,
        Principals: Sequence[SharePrincipalTypeDef],
        AuthenticationToken: str = ...,
        NotificationOptions: NotificationOptionsTypeDef = ...,
    ) -> AddResourcePermissionsResponseTypeDef:
        """
        Creates a set of permissions for the specified folder or document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.add_resource_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#add_resource_permissions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#close)
        """

    async def create_comment(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        Text: str,
        AuthenticationToken: str = ...,
        ParentId: str = ...,
        ThreadId: str = ...,
        Visibility: CommentVisibilityTypeType = ...,
        NotifyCollaborators: bool = ...,
    ) -> CreateCommentResponseTypeDef:
        """
        Adds a new comment to the specified document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_comment)
        """

    async def create_custom_metadata(
        self,
        *,
        ResourceId: str,
        CustomMetadata: Mapping[str, str],
        AuthenticationToken: str = ...,
        VersionId: str = ...,
    ) -> Dict[str, Any]:
        """
        Adds one or more custom properties to the specified resource (a folder,
        document, or
        version).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_custom_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_custom_metadata)
        """

    async def create_folder(
        self, *, ParentFolderId: str, AuthenticationToken: str = ..., Name: str = ...
    ) -> CreateFolderResponseTypeDef:
        """
        Creates a folder with the specified name and parent folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_folder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_folder)
        """

    async def create_labels(
        self, *, ResourceId: str, Labels: Sequence[str], AuthenticationToken: str = ...
    ) -> Dict[str, Any]:
        """
        Adds the specified list of labels to the given resource (a document or folder)
        See also: [AWS API
        Documentation](https://docs.aws.amazon.com/goto/WebAPI/workdocs-2016-05-01/CreateLabels).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_labels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_labels)
        """

    async def create_notification_subscription(
        self,
        *,
        OrganizationId: str,
        Endpoint: str,
        Protocol: SubscriptionProtocolTypeType,
        SubscriptionType: Literal["ALL"],
    ) -> CreateNotificationSubscriptionResponseTypeDef:
        """
        Configure Amazon WorkDocs to use Amazon SNS notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_notification_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_notification_subscription)
        """

    async def create_user(
        self,
        *,
        Username: str,
        GivenName: str,
        Surname: str,
        Password: str,
        OrganizationId: str = ...,
        EmailAddress: str = ...,
        TimeZoneId: str = ...,
        StorageRule: StorageRuleTypeTypeDef = ...,
        AuthenticationToken: str = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a user in a Simple AD or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#create_user)
        """

    async def deactivate_user(
        self, *, UserId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deactivates the specified user, which revokes the user's access to Amazon
        WorkDocs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.deactivate_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#deactivate_user)
        """

    async def delete_comment(
        self, *, DocumentId: str, VersionId: str, CommentId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified comment from the document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_comment)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_comment)
        """

    async def delete_custom_metadata(
        self,
        *,
        ResourceId: str,
        AuthenticationToken: str = ...,
        VersionId: str = ...,
        Keys: Sequence[str] = ...,
        DeleteAll: bool = ...,
    ) -> Dict[str, Any]:
        """
        Deletes custom metadata from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_custom_metadata)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_custom_metadata)
        """

    async def delete_document(
        self, *, DocumentId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes the specified document and its associated metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_document)
        """

    async def delete_document_version(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        DeletePriorVersions: bool,
        AuthenticationToken: str = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a specific version of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_document_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_document_version)
        """

    async def delete_folder(
        self, *, FolderId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Permanently deletes the specified folder and its contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_folder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_folder)
        """

    async def delete_folder_contents(
        self, *, FolderId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the contents of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_folder_contents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_folder_contents)
        """

    async def delete_labels(
        self,
        *,
        ResourceId: str,
        AuthenticationToken: str = ...,
        Labels: Sequence[str] = ...,
        DeleteAll: bool = ...,
    ) -> Dict[str, Any]:
        """
        Deletes the specified list of labels from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_labels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_labels)
        """

    async def delete_notification_subscription(
        self, *, SubscriptionId: str, OrganizationId: str
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified subscription from the specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_notification_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_notification_subscription)
        """

    async def delete_user(
        self, *, UserId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified user from a Simple AD or Microsoft AD directory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.delete_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#delete_user)
        """

    async def describe_activities(
        self,
        *,
        AuthenticationToken: str = ...,
        StartTime: TimestampTypeDef = ...,
        EndTime: TimestampTypeDef = ...,
        OrganizationId: str = ...,
        ActivityTypes: str = ...,
        ResourceId: str = ...,
        UserId: str = ...,
        IncludeIndirectActivities: bool = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> DescribeActivitiesResponseTypeDef:
        """
        Describes the user activities in a specified time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_activities)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_activities)
        """

    async def describe_comments(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        AuthenticationToken: str = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> DescribeCommentsResponseTypeDef:
        """
        List all the comments for the specified document version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_comments)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_comments)
        """

    async def describe_document_versions(
        self,
        *,
        DocumentId: str,
        AuthenticationToken: str = ...,
        Marker: str = ...,
        Limit: int = ...,
        Include: str = ...,
        Fields: str = ...,
    ) -> DescribeDocumentVersionsResponseTypeDef:
        """
        Retrieves the document versions for the specified document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_document_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_document_versions)
        """

    async def describe_folder_contents(
        self,
        *,
        FolderId: str,
        AuthenticationToken: str = ...,
        Sort: ResourceSortTypeType = ...,
        Order: OrderTypeType = ...,
        Limit: int = ...,
        Marker: str = ...,
        Type: FolderContentTypeType = ...,
        Include: str = ...,
    ) -> DescribeFolderContentsResponseTypeDef:
        """
        Describes the contents of the specified folder, including its documents and
        subfolders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_folder_contents)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_folder_contents)
        """

    async def describe_groups(
        self,
        *,
        SearchQuery: str,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        Marker: str = ...,
        Limit: int = ...,
    ) -> DescribeGroupsResponseTypeDef:
        """
        Describes the groups specified by the query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_groups)
        """

    async def describe_notification_subscriptions(
        self, *, OrganizationId: str, Marker: str = ..., Limit: int = ...
    ) -> DescribeNotificationSubscriptionsResponseTypeDef:
        """
        Lists the specified notification subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_notification_subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_notification_subscriptions)
        """

    async def describe_resource_permissions(
        self,
        *,
        ResourceId: str,
        AuthenticationToken: str = ...,
        PrincipalId: str = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> DescribeResourcePermissionsResponseTypeDef:
        """
        Describes the permissions of a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_resource_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_resource_permissions)
        """

    async def describe_root_folders(
        self, *, AuthenticationToken: str, Limit: int = ..., Marker: str = ...
    ) -> DescribeRootFoldersResponseTypeDef:
        """
        Describes the current user's special folders; the `RootFolder` and the
        `RecycleBin`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_root_folders)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_root_folders)
        """

    async def describe_users(
        self,
        *,
        AuthenticationToken: str = ...,
        OrganizationId: str = ...,
        UserIds: str = ...,
        Query: str = ...,
        Include: UserFilterTypeType = ...,
        Order: OrderTypeType = ...,
        Sort: UserSortTypeType = ...,
        Marker: str = ...,
        Limit: int = ...,
        Fields: str = ...,
    ) -> DescribeUsersResponseTypeDef:
        """
        Describes the specified users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.describe_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#describe_users)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#generate_presigned_url)
        """

    async def get_current_user(self, *, AuthenticationToken: str) -> GetCurrentUserResponseTypeDef:
        """
        Retrieves details of the current user for whom the authentication token was
        generated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_current_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_current_user)
        """

    async def get_document(
        self, *, DocumentId: str, AuthenticationToken: str = ..., IncludeCustomMetadata: bool = ...
    ) -> GetDocumentResponseTypeDef:
        """
        Retrieves details of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_document)
        """

    async def get_document_path(
        self,
        *,
        DocumentId: str,
        AuthenticationToken: str = ...,
        Limit: int = ...,
        Fields: str = ...,
        Marker: str = ...,
    ) -> GetDocumentPathResponseTypeDef:
        """
        Retrieves the path information (the hierarchy from the root folder) for the
        requested
        document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document_path)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_document_path)
        """

    async def get_document_version(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        AuthenticationToken: str = ...,
        Fields: str = ...,
        IncludeCustomMetadata: bool = ...,
    ) -> GetDocumentVersionResponseTypeDef:
        """
        Retrieves version metadata for the specified document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_document_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_document_version)
        """

    async def get_folder(
        self, *, FolderId: str, AuthenticationToken: str = ..., IncludeCustomMetadata: bool = ...
    ) -> GetFolderResponseTypeDef:
        """
        Retrieves the metadata of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_folder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_folder)
        """

    async def get_folder_path(
        self,
        *,
        FolderId: str,
        AuthenticationToken: str = ...,
        Limit: int = ...,
        Fields: str = ...,
        Marker: str = ...,
    ) -> GetFolderPathResponseTypeDef:
        """
        Retrieves the path information (the hierarchy from the root folder) for the
        specified
        folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_folder_path)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_folder_path)
        """

    async def get_resources(
        self,
        *,
        AuthenticationToken: str = ...,
        UserId: str = ...,
        CollectionType: Literal["SHARED_WITH_ME"] = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> GetResourcesResponseTypeDef:
        """
        Retrieves a collection of resources, including folders and documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_resources)
        """

    async def initiate_document_version_upload(
        self,
        *,
        AuthenticationToken: str = ...,
        Id: str = ...,
        Name: str = ...,
        ContentCreatedTimestamp: TimestampTypeDef = ...,
        ContentModifiedTimestamp: TimestampTypeDef = ...,
        ContentType: str = ...,
        DocumentSizeInBytes: int = ...,
        ParentFolderId: str = ...,
    ) -> InitiateDocumentVersionUploadResponseTypeDef:
        """
        Creates a new document object and version object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.initiate_document_version_upload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#initiate_document_version_upload)
        """

    async def remove_all_resource_permissions(
        self, *, ResourceId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes all the permissions from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.remove_all_resource_permissions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#remove_all_resource_permissions)
        """

    async def remove_resource_permission(
        self,
        *,
        ResourceId: str,
        PrincipalId: str,
        AuthenticationToken: str = ...,
        PrincipalType: PrincipalTypeType = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the permission for the specified principal from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.remove_resource_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#remove_resource_permission)
        """

    async def restore_document_versions(
        self, *, DocumentId: str, AuthenticationToken: str = ...
    ) -> EmptyResponseMetadataTypeDef:
        """
        Recovers a deleted version of an Amazon WorkDocs document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.restore_document_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#restore_document_versions)
        """

    async def search_resources(
        self,
        *,
        AuthenticationToken: str = ...,
        QueryText: str = ...,
        QueryScopes: Sequence[SearchQueryScopeTypeType] = ...,
        OrganizationId: str = ...,
        AdditionalResponseFields: Sequence[Literal["WEBURL"]] = ...,
        Filters: FiltersTypeDef = ...,
        OrderBy: Sequence[SearchSortResultTypeDef] = ...,
        Limit: int = ...,
        Marker: str = ...,
    ) -> SearchResourcesResponseTypeDef:
        """
        Searches metadata and the content of folders, documents, document versions, and
        comments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.search_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#search_resources)
        """

    async def update_document(
        self,
        *,
        DocumentId: str,
        AuthenticationToken: str = ...,
        Name: str = ...,
        ParentFolderId: str = ...,
        ResourceState: ResourceStateTypeType = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the specified attributes of a document.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_document)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#update_document)
        """

    async def update_document_version(
        self,
        *,
        DocumentId: str,
        VersionId: str,
        AuthenticationToken: str = ...,
        VersionStatus: Literal["ACTIVE"] = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the status of the document version to ACTIVE.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_document_version)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#update_document_version)
        """

    async def update_folder(
        self,
        *,
        FolderId: str,
        AuthenticationToken: str = ...,
        Name: str = ...,
        ParentFolderId: str = ...,
        ResourceState: ResourceStateTypeType = ...,
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the specified attributes of the specified folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_folder)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#update_folder)
        """

    async def update_user(
        self,
        *,
        UserId: str,
        AuthenticationToken: str = ...,
        GivenName: str = ...,
        Surname: str = ...,
        Type: UserTypeType = ...,
        StorageRule: StorageRuleTypeTypeDef = ...,
        TimeZoneId: str = ...,
        Locale: LocaleTypeType = ...,
        GrantPoweruserPrivileges: BooleanEnumTypeType = ...,
    ) -> UpdateUserResponseTypeDef:
        """
        Updates the specified attributes of the specified user, and grants or revokes
        administrative privileges to the Amazon WorkDocs
        site.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#update_user)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_activities"]
    ) -> DescribeActivitiesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_comments"]
    ) -> DescribeCommentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_document_versions"]
    ) -> DescribeDocumentVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_folder_contents"]
    ) -> DescribeFolderContentsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_groups"]) -> DescribeGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_notification_subscriptions"]
    ) -> DescribeNotificationSubscriptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_resource_permissions"]
    ) -> DescribeResourcePermissionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_root_folders"]
    ) -> DescribeRootFoldersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["describe_users"]) -> DescribeUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["search_resources"]
    ) -> SearchResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/#get_paginator)
        """

    async def __aenter__(self) -> "WorkDocsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workdocs.html#WorkDocs.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workdocs/client/)
        """
