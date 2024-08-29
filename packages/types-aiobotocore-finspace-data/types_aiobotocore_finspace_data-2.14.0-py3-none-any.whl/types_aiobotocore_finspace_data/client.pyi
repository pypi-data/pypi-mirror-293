"""
Type annotations for finspace-data service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace_data.client import FinSpaceDataClient

    session = get_session()
    async with session.create_client("finspace-data") as client:
        client: FinSpaceDataClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    ApiAccessType,
    ApplicationPermissionType,
    ChangeTypeType,
    DatasetKindType,
    LocationTypeType,
    UserTypeType,
)
from .paginator import (
    ListChangesetsPaginator,
    ListDatasetsPaginator,
    ListDataViewsPaginator,
    ListPermissionGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssociateUserToPermissionGroupResponseTypeDef,
    CreateChangesetResponseTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDataViewResponseTypeDef,
    CreatePermissionGroupResponseTypeDef,
    CreateUserResponseTypeDef,
    DatasetOwnerInfoTypeDef,
    DataViewDestinationTypeParamsUnionTypeDef,
    DeleteDatasetResponseTypeDef,
    DeletePermissionGroupResponseTypeDef,
    DisableUserResponseTypeDef,
    DisassociateUserFromPermissionGroupResponseTypeDef,
    EnableUserResponseTypeDef,
    GetChangesetResponseTypeDef,
    GetDatasetResponseTypeDef,
    GetDataViewResponseTypeDef,
    GetExternalDataViewAccessDetailsResponseTypeDef,
    GetPermissionGroupResponseTypeDef,
    GetProgrammaticAccessCredentialsResponseTypeDef,
    GetUserResponseTypeDef,
    GetWorkingLocationResponseTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsByUserResponseTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersByPermissionGroupResponseTypeDef,
    ListUsersResponseTypeDef,
    PermissionGroupParamsTypeDef,
    ResetUserPasswordResponseTypeDef,
    SchemaUnionUnionTypeDef,
    UpdateChangesetResponseTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdatePermissionGroupResponseTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("FinSpaceDataClient",)

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
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class FinSpaceDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinSpaceDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#exceptions)
        """

    async def associate_user_to_permission_group(
        self, *, permissionGroupId: str, userId: str, clientToken: str = ...
    ) -> AssociateUserToPermissionGroupResponseTypeDef:
        """
        Adds a user to a permission group to grant permissions for actions a user can
        perform in
        FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.associate_user_to_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#associate_user_to_permission_group)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#close)
        """

    async def create_changeset(
        self,
        *,
        datasetId: str,
        changeType: ChangeTypeType,
        sourceParams: Mapping[str, str],
        formatParams: Mapping[str, str],
        clientToken: str = ...,
    ) -> CreateChangesetResponseTypeDef:
        """
        Creates a new Changeset in a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_changeset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_changeset)
        """

    async def create_data_view(
        self,
        *,
        datasetId: str,
        destinationTypeParams: DataViewDestinationTypeParamsUnionTypeDef,
        clientToken: str = ...,
        autoUpdate: bool = ...,
        sortColumns: Sequence[str] = ...,
        partitionColumns: Sequence[str] = ...,
        asOfTimestamp: int = ...,
    ) -> CreateDataViewResponseTypeDef:
        """
        Creates a Dataview for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_data_view)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_data_view)
        """

    async def create_dataset(
        self,
        *,
        datasetTitle: str,
        kind: DatasetKindType,
        permissionGroupParams: PermissionGroupParamsTypeDef,
        clientToken: str = ...,
        datasetDescription: str = ...,
        ownerInfo: DatasetOwnerInfoTypeDef = ...,
        alias: str = ...,
        schemaDefinition: SchemaUnionUnionTypeDef = ...,
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_dataset)
        """

    async def create_permission_group(
        self,
        *,
        name: str,
        applicationPermissions: Sequence[ApplicationPermissionType],
        description: str = ...,
        clientToken: str = ...,
    ) -> CreatePermissionGroupResponseTypeDef:
        """
        Creates a group of permissions for various actions that a user can perform in
        FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_permission_group)
        """

    async def create_user(
        self,
        *,
        emailAddress: str,
        type: UserTypeType,
        firstName: str = ...,
        lastName: str = ...,
        apiAccess: ApiAccessType = ...,
        apiAccessPrincipalArn: str = ...,
        clientToken: str = ...,
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new user in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.create_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_user)
        """

    async def delete_dataset(
        self, *, datasetId: str, clientToken: str = ...
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.delete_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#delete_dataset)
        """

    async def delete_permission_group(
        self, *, permissionGroupId: str, clientToken: str = ...
    ) -> DeletePermissionGroupResponseTypeDef:
        """
        Deletes a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.delete_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#delete_permission_group)
        """

    async def disable_user(
        self, *, userId: str, clientToken: str = ...
    ) -> DisableUserResponseTypeDef:
        """
        Denies access to the FinSpace web application and API for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.disable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#disable_user)
        """

    async def disassociate_user_from_permission_group(
        self, *, permissionGroupId: str, userId: str, clientToken: str = ...
    ) -> DisassociateUserFromPermissionGroupResponseTypeDef:
        """
        Removes a user from a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.disassociate_user_from_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#disassociate_user_from_permission_group)
        """

    async def enable_user(
        self, *, userId: str, clientToken: str = ...
    ) -> EnableUserResponseTypeDef:
        """
        Allows the specified user to access the FinSpace web application and API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.enable_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#enable_user)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#generate_presigned_url)
        """

    async def get_changeset(
        self, *, datasetId: str, changesetId: str
    ) -> GetChangesetResponseTypeDef:
        """
        Get information about a Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_changeset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_changeset)
        """

    async def get_data_view(self, *, dataViewId: str, datasetId: str) -> GetDataViewResponseTypeDef:
        """
        Gets information about a Dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_data_view)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_data_view)
        """

    async def get_dataset(self, *, datasetId: str) -> GetDatasetResponseTypeDef:
        """
        Returns information about a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_dataset)
        """

    async def get_external_data_view_access_details(
        self, *, dataViewId: str, datasetId: str
    ) -> GetExternalDataViewAccessDetailsResponseTypeDef:
        """
        Returns the credentials to access the external Dataview from an S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_external_data_view_access_details)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_external_data_view_access_details)
        """

    async def get_permission_group(
        self, *, permissionGroupId: str
    ) -> GetPermissionGroupResponseTypeDef:
        """
        Retrieves the details of a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_permission_group)
        """

    async def get_programmatic_access_credentials(
        self, *, environmentId: str, durationInMinutes: int = ...
    ) -> GetProgrammaticAccessCredentialsResponseTypeDef:
        """
        Request programmatic credentials to use with FinSpace SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_programmatic_access_credentials)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_programmatic_access_credentials)
        """

    async def get_user(self, *, userId: str) -> GetUserResponseTypeDef:
        """
        Retrieves details for a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_user)
        """

    async def get_working_location(
        self, *, locationType: LocationTypeType = ...
    ) -> GetWorkingLocationResponseTypeDef:
        """
        A temporary Amazon S3 location, where you can copy your files from a source
        location to stage or use as a scratch space in FinSpace
        notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_working_location)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_working_location)
        """

    async def list_changesets(
        self, *, datasetId: str, maxResults: int = ..., nextToken: str = ...
    ) -> ListChangesetsResponseTypeDef:
        """
        Lists the FinSpace Changesets for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_changesets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_changesets)
        """

    async def list_data_views(
        self, *, datasetId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListDataViewsResponseTypeDef:
        """
        Lists all available Dataviews for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_data_views)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_data_views)
        """

    async def list_datasets(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the active Datasets that a user has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_datasets)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_datasets)
        """

    async def list_permission_groups(
        self, *, maxResults: int, nextToken: str = ...
    ) -> ListPermissionGroupsResponseTypeDef:
        """
        Lists all available permission groups in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_permission_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_permission_groups)
        """

    async def list_permission_groups_by_user(
        self, *, userId: str, maxResults: int, nextToken: str = ...
    ) -> ListPermissionGroupsByUserResponseTypeDef:
        """
        Lists all the permission groups that are associated with a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_permission_groups_by_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_permission_groups_by_user)
        """

    async def list_users(
        self, *, maxResults: int, nextToken: str = ...
    ) -> ListUsersResponseTypeDef:
        """
        Lists all available users in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_users)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_users)
        """

    async def list_users_by_permission_group(
        self, *, permissionGroupId: str, maxResults: int, nextToken: str = ...
    ) -> ListUsersByPermissionGroupResponseTypeDef:
        """
        Lists details of all the users in a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.list_users_by_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_users_by_permission_group)
        """

    async def reset_user_password(
        self, *, userId: str, clientToken: str = ...
    ) -> ResetUserPasswordResponseTypeDef:
        """
        Resets the password for a specified user ID and generates a temporary one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.reset_user_password)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#reset_user_password)
        """

    async def update_changeset(
        self,
        *,
        datasetId: str,
        changesetId: str,
        sourceParams: Mapping[str, str],
        formatParams: Mapping[str, str],
        clientToken: str = ...,
    ) -> UpdateChangesetResponseTypeDef:
        """
        Updates a FinSpace Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_changeset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_changeset)
        """

    async def update_dataset(
        self,
        *,
        datasetId: str,
        datasetTitle: str,
        kind: DatasetKindType,
        clientToken: str = ...,
        datasetDescription: str = ...,
        alias: str = ...,
        schemaDefinition: SchemaUnionUnionTypeDef = ...,
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_dataset)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_dataset)
        """

    async def update_permission_group(
        self,
        *,
        permissionGroupId: str,
        name: str = ...,
        description: str = ...,
        applicationPermissions: Sequence[ApplicationPermissionType] = ...,
        clientToken: str = ...,
    ) -> UpdatePermissionGroupResponseTypeDef:
        """
        Modifies the details of a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_permission_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_permission_group)
        """

    async def update_user(
        self,
        *,
        userId: str,
        type: UserTypeType = ...,
        firstName: str = ...,
        lastName: str = ...,
        apiAccess: ApiAccessType = ...,
        apiAccessPrincipalArn: str = ...,
        clientToken: str = ...,
    ) -> UpdateUserResponseTypeDef:
        """
        Modifies the details of the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.update_user)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_user)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_changesets"]) -> ListChangesetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_data_views"]) -> ListDataViewsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_datasets"]) -> ListDatasetsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_permission_groups"]
    ) -> ListPermissionGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_users"]) -> ListUsersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    async def __aenter__(self) -> "FinSpaceDataClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
        """
