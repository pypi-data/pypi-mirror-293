"""
Type annotations for codestar service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codestar.client import CodeStarClient

    session = get_session()
    async with session.create_client("codestar") as client:
        client: CodeStarClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListProjectsPaginator,
    ListResourcesPaginator,
    ListTeamMembersPaginator,
    ListUserProfilesPaginator,
)
from .type_defs import (
    AssociateTeamMemberRequestRequestTypeDef,
    AssociateTeamMemberResultTypeDef,
    CreateProjectRequestRequestTypeDef,
    CreateProjectResultTypeDef,
    CreateUserProfileRequestRequestTypeDef,
    CreateUserProfileResultTypeDef,
    DeleteProjectRequestRequestTypeDef,
    DeleteProjectResultTypeDef,
    DeleteUserProfileRequestRequestTypeDef,
    DeleteUserProfileResultTypeDef,
    DescribeProjectRequestRequestTypeDef,
    DescribeProjectResultTypeDef,
    DescribeUserProfileRequestRequestTypeDef,
    DescribeUserProfileResultTypeDef,
    DisassociateTeamMemberRequestRequestTypeDef,
    ListProjectsRequestRequestTypeDef,
    ListProjectsResultTypeDef,
    ListResourcesRequestRequestTypeDef,
    ListResourcesResultTypeDef,
    ListTagsForProjectRequestRequestTypeDef,
    ListTagsForProjectResultTypeDef,
    ListTeamMembersRequestRequestTypeDef,
    ListTeamMembersResultTypeDef,
    ListUserProfilesRequestRequestTypeDef,
    ListUserProfilesResultTypeDef,
    TagProjectRequestRequestTypeDef,
    TagProjectResultTypeDef,
    UntagProjectRequestRequestTypeDef,
    UpdateProjectRequestRequestTypeDef,
    UpdateTeamMemberRequestRequestTypeDef,
    UpdateTeamMemberResultTypeDef,
    UpdateUserProfileRequestRequestTypeDef,
    UpdateUserProfileResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("CodeStarClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    InvalidServiceRoleException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ProjectAlreadyExistsException: Type[BotocoreClientError]
    ProjectConfigurationException: Type[BotocoreClientError]
    ProjectCreationFailedException: Type[BotocoreClientError]
    ProjectNotFoundException: Type[BotocoreClientError]
    TeamMemberAlreadyAssociatedException: Type[BotocoreClientError]
    TeamMemberNotFoundException: Type[BotocoreClientError]
    UserProfileAlreadyExistsException: Type[BotocoreClientError]
    UserProfileNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CodeStarClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeStarClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#exceptions)
        """

    async def associate_team_member(
        self, **kwargs: Unpack[AssociateTeamMemberRequestRequestTypeDef]
    ) -> AssociateTeamMemberResultTypeDef:
        """
        Adds an IAM user to the team for an AWS CodeStar project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.associate_team_member)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#associate_team_member)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#close)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectRequestRequestTypeDef]
    ) -> CreateProjectResultTypeDef:
        """
        Creates a project, including project resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.create_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#create_project)
        """

    async def create_user_profile(
        self, **kwargs: Unpack[CreateUserProfileRequestRequestTypeDef]
    ) -> CreateUserProfileResultTypeDef:
        """
        Creates a profile for a user that includes user preferences, such as the
        display name and email address assocciated with the user, in AWS
        CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.create_user_profile)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#create_user_profile)
        """

    async def delete_project(
        self, **kwargs: Unpack[DeleteProjectRequestRequestTypeDef]
    ) -> DeleteProjectResultTypeDef:
        """
        Deletes a project, including project resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.delete_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#delete_project)
        """

    async def delete_user_profile(
        self, **kwargs: Unpack[DeleteUserProfileRequestRequestTypeDef]
    ) -> DeleteUserProfileResultTypeDef:
        """
        Deletes a user profile in AWS CodeStar, including all personal preference data
        associated with that profile, such as display name and email
        address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.delete_user_profile)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#delete_user_profile)
        """

    async def describe_project(
        self, **kwargs: Unpack[DescribeProjectRequestRequestTypeDef]
    ) -> DescribeProjectResultTypeDef:
        """
        Describes a project and its resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.describe_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#describe_project)
        """

    async def describe_user_profile(
        self, **kwargs: Unpack[DescribeUserProfileRequestRequestTypeDef]
    ) -> DescribeUserProfileResultTypeDef:
        """
        Describes a user in AWS CodeStar and the user attributes across all projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.describe_user_profile)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#describe_user_profile)
        """

    async def disassociate_team_member(
        self, **kwargs: Unpack[DisassociateTeamMemberRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a user from a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.disassociate_team_member)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#disassociate_team_member)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#generate_presigned_url)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsRequestRequestTypeDef]
    ) -> ListProjectsResultTypeDef:
        """
        Lists all projects in AWS CodeStar associated with your AWS account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_projects)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#list_projects)
        """

    async def list_resources(
        self, **kwargs: Unpack[ListResourcesRequestRequestTypeDef]
    ) -> ListResourcesResultTypeDef:
        """
        Lists resources associated with a project in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_resources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#list_resources)
        """

    async def list_tags_for_project(
        self, **kwargs: Unpack[ListTagsForProjectRequestRequestTypeDef]
    ) -> ListTagsForProjectResultTypeDef:
        """
        Gets the tags for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_tags_for_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#list_tags_for_project)
        """

    async def list_team_members(
        self, **kwargs: Unpack[ListTeamMembersRequestRequestTypeDef]
    ) -> ListTeamMembersResultTypeDef:
        """
        Lists all team members associated with a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_team_members)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#list_team_members)
        """

    async def list_user_profiles(
        self, **kwargs: Unpack[ListUserProfilesRequestRequestTypeDef]
    ) -> ListUserProfilesResultTypeDef:
        """
        Lists all the user profiles configured for your AWS account in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.list_user_profiles)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#list_user_profiles)
        """

    async def tag_project(
        self, **kwargs: Unpack[TagProjectRequestRequestTypeDef]
    ) -> TagProjectResultTypeDef:
        """
        Adds tags to a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.tag_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#tag_project)
        """

    async def untag_project(
        self, **kwargs: Unpack[UntagProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.untag_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#untag_project)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a project in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_project)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#update_project)
        """

    async def update_team_member(
        self, **kwargs: Unpack[UpdateTeamMemberRequestRequestTypeDef]
    ) -> UpdateTeamMemberResultTypeDef:
        """
        Updates a team member's attributes in an AWS CodeStar project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_team_member)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#update_team_member)
        """

    async def update_user_profile(
        self, **kwargs: Unpack[UpdateUserProfileRequestRequestTypeDef]
    ) -> UpdateUserProfileResultTypeDef:
        """
        Updates a user's profile in AWS CodeStar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.update_user_profile)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#update_user_profile)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_projects"]) -> ListProjectsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_resources"]) -> ListResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_team_members"]
    ) -> ListTeamMembersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_user_profiles"]
    ) -> ListUserProfilesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/#get_paginator)
        """

    async def __aenter__(self) -> "CodeStarClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codestar.html#CodeStar.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codestar/client/)
        """
