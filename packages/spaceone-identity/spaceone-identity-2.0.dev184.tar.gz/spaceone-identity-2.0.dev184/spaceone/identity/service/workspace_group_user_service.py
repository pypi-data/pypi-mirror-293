from typing import Union

from spaceone.core.service import (
    BaseService,
    authentication_handler,
    authorization_handler,
    event_handler,
    mutation_handler,
    transaction,
)
from spaceone.core.service.utils import (
    append_keyword_filter,
    append_query_filter,
    convert_model,
)

from spaceone.identity.manager.user_manager import UserManager
from spaceone.identity.manager.workspace_group_manager import WorkspaceGroupManager
from spaceone.identity.manager.workspace_group_user_manager import (
    WorkspaceGroupUserManager,
)
from spaceone.identity.model.workspace_group_user.request import (
    WorkspaceGroupUserAddRequest,
    WorkspaceGroupUserFindRequest,
    WorkspaceGroupUserGetRequest,
    WorkspaceGroupUserRemoveRequest,
    WorkspaceGroupUserSearchQueryRequest,
    WorkspaceGroupUserStatQueryRequest,
    WorkspaceGroupUserUpdateRoleRequest,
)
from spaceone.identity.model.workspace_group_user.response import (
    WorkspaceGroupUserResponse,
    WorkspaceGroupUsersResponse,
    WorkspaceGroupUsersSummaryResponse,
)


@authentication_handler
@authorization_handler
@mutation_handler
@event_handler
class WorkspaceGroupUserService(BaseService):
    resource = "WorkspaceGroupUser"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace_group_mgr = WorkspaceGroupManager()
        self.workspace_group_user_mgr = WorkspaceGroupUserManager()

    @transaction(permission="identity:WorkspaceGroupUser:write", role_types=["USER"])
    @convert_model
    def add(
        self, params: WorkspaceGroupUserAddRequest
    ) -> Union[WorkspaceGroupUserResponse, dict]:
        """Add workspace group user
        Args:
            params (WorkspaceGroupUserAddRequest): {
                'workspace_group_id': 'str',     # required
                'users': [
                    {
                        'user_id': 'str',        # required
                        'role_id': 'str',        # required
                    }
                ],
                'user_id': 'str',                # injected from auth (required)
                'domain_id': 'str',              # injected from auth (required)
            }
        Returns:
           WorkspaceGroupUserResponse:
        """
        pass

    @transaction(permission="identity:WorkspaceGroupUser:write", role_types=["USER"])
    @convert_model
    def remove(
        self, params: WorkspaceGroupUserRemoveRequest
    ) -> Union[WorkspaceGroupUserResponse, dict]:
        """Remove workspace group user
        Args:
            params (WorkspaceGroupUserRemoveRequest): {
                'workspace_group_id': 'str',        # required
                'users': [
                    {
                        'user_id': 'str',           # required
                    }
                ],
                'user_id': 'str',                   # injected from auth (required)
                'domain_id': 'str',                 # injected from auth (required)
            }
        Returns:
            WorkspaceGroupUserResponse:
        """
        pass

    @transaction(permission="identity:WorkspaceGroupUser:write", role_types=["USER"])
    @convert_model
    def update_role(
        self, params: WorkspaceGroupUserUpdateRoleRequest
    ) -> Union[WorkspaceGroupUserResponse, dict]:
        """Update workspace group user role
        Args:
            params (WorkspaceGroupUserUpdateRoleRequest): {
                'workspace_group_id': 'str',            # required
                'role_id': 'str',                       # required
                'user_id': 'str',                       # injected from auth (required)
                'domain_id': 'str',                     # injected from auth (required)
            }
        Returns:
            WorkspaceGroupUserResponse:
        """
        pass

    @transaction(permission="identity:WorkspaceGroupUser:read", role_types=["USER"])
    @convert_model
    def find(
        self, params: WorkspaceGroupUserFindRequest
    ) -> Union[WorkspaceGroupUsersSummaryResponse, dict]:
        """Find users in the domain except users in its workspace_group
        Args:
            params (WorkspaceGroupUserFindRequest): {
                'workspace_group_id': 'str',      # required
                'keyword': 'str',
                'state': 'State',
                'page': 'dict',
                'user_id': 'str'                  # injected from auth (required)
                'domain_id': 'str',               # injected from auth (required)
            }
        Returns:
            WorkspaceGroupUsersSummaryResponse:
        """
        return self._find(params)

    @transaction(permission="identity:WorkspaceGroupUser:read", role_types=["USER"])
    @convert_model
    def get(
        self, params: WorkspaceGroupUserGetRequest
    ) -> Union[WorkspaceGroupUserResponse, dict]:
        """Get workspace groups
        Args:
            params (WorkspaceGroupUserGetRequest): {
                'workspace_group_id': 'str',     # required
                'user_id': 'str'                 # injected from auth (required)
                'domain_id': 'str',              # injected from auth (required)
            }
        Returns:
            WorkspaceGroupUserResponse:
        """
        user_info = self.workspace_group_user_mgr.get_workspace_group_user(
            params.user_id, params.workspace_group_id, params.domain_id
        )
        return WorkspaceGroupUserResponse(**user_info)

    @transaction(permission="identity:WorkspaceGroupUser.read", role_types=["USER"])
    @append_query_filter(["user_id", "workspace_group_id", "name", "domain_id"])
    @append_keyword_filter(["user_id", "workspace_group_id", "name"])
    @convert_model
    def list(
        self, params: WorkspaceGroupUserSearchQueryRequest
    ) -> Union[WorkspaceGroupUsersResponse, dict]:
        """List workspace group users
        Args:
            params (WorkspaceGroupUserSearchQueryRequest): {
                'query': 'dict (spaceone.api.core.v1.Query)',
                'workspace_group_id': 'str',
                'name': 'str',
                'created_by': 'str',
                'updated_by': 'str',
                'user_id': 'str'                         # injected from auth (required)
                'domain_id': 'str',                      # injected from auth (required)
            }
        Returns:
            WorkspaceGroupUsersResponse:
        """
        query = params.query or {}
        users_info, total_count = (
            self.workspace_group_user_mgr.list_workspace_group_users(
                query, params.domain_id, params.workspace_group_id
            )
        )

        return WorkspaceGroupUsersResponse(results=users_info, total_count=total_count)

    @transaction(permission="identity:WorkspaceGroup.read", role_types=["USER"])
    @append_query_filter(["user_id", "workspace_group_id", "domain_id"])
    @convert_model
    def stat(self, params: WorkspaceGroupUserStatQueryRequest) -> dict:
        """Stat workspace group users
        Args:
            params (WorkspaceGroupUserStatQueryRequest): {
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)', # required
                'workspace_group_id': 'str',           # required
                'user_id': 'str'                       # injected from auth (required)
                'domain_id': 'str',                    # injected from auth (required)
            }
        Returns:
            dict: {
                'results': 'list',
                'total_count': 'int'
            }
        """
        query = params.query or {}

        return self.workspace_group_user_mgr.stat_workspace_group_users(
            query, params.workspace_group_id, params.domain_id
        )

    def _find(
        self, params: WorkspaceGroupUserFindRequest
    ) -> Union[WorkspaceGroupUsersSummaryResponse, dict]:
        workspace_group = self.workspace_group_mgr.get_workspace_group(
            params.workspace_group_id, params.domain_id
        )
        workspace_group_users = workspace_group.users or []
        workspace_group_user_ids = list(
            set([user["user_id"] for user in workspace_group_users])
        )

        query = {
            "filter": [
                {"k": "domain_id", "v": params.domain_id, "o": "eq"},
                {"k": "user_id", "v": workspace_group_user_ids, "o": "not_in"},
            ],
            "sort": [{"key": "user_id"}],
            "page": params.page,
            "only": ["user_id", "name", "state"],
        }

        if params.keyword:
            query["filter_or"] = [
                {"k": "user_id", "v": params.keyword, "o": "contain"},
                {"k": "name", "v": params.keyword, "o": "contain"},
            ]

        if params.state:
            query["filter"].append({"k": "state", "v": params.state, "o": "eq"})

        user_mgr = UserManager()
        user_vos, total_count = user_mgr.list_users(query)

        workspace_group_users_info = [user_vo.to_dict() for user_vo in user_vos]

        return WorkspaceGroupUsersSummaryResponse(
            results=workspace_group_users_info, total_count=total_count
        )
