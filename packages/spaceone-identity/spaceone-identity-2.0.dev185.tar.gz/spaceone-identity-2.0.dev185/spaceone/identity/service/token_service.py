import logging
from typing import List, Tuple

from spaceone.core import cache
from spaceone.core.auth.jwt import JWTAuthenticator, JWTUtil
from spaceone.core.service import *
from spaceone.core.service.utils import *

from spaceone.identity.error.error_authentication import *
from spaceone.identity.error.error_domain import ERROR_DOMAIN_STATE
from spaceone.identity.error.error_mfa import *
from spaceone.identity.error.error_workspace import ERROR_WORKSPACE_STATE
from spaceone.identity.manager.app_manager import AppManager
from spaceone.identity.manager.domain_manager import DomainManager
from spaceone.identity.manager.domain_secret_manager import DomainSecretManager
from spaceone.identity.manager.mfa_manager.base import MFAManager
from spaceone.identity.manager.project_group_manager import ProjectGroupManager
from spaceone.identity.manager.project_manager import ProjectManager
from spaceone.identity.manager.role_binding_manager import RoleBindingManager
from spaceone.identity.manager.role_manager import RoleManager
from spaceone.identity.manager.system_manager import SystemManager
from spaceone.identity.manager.token_manager.base import TokenManager
from spaceone.identity.manager.user_manager import UserManager
from spaceone.identity.manager.workspace_manager import WorkspaceManager
from spaceone.identity.model.app.database import App
from spaceone.identity.model.token.request import *
from spaceone.identity.model.token.response import *
from spaceone.identity.model.user.database import User

_LOGGER = logging.getLogger(__name__)


@event_handler
class TokenService(BaseService):
    resource = "Token"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_mgr = DomainManager()
        self.domain_secret_mgr = DomainSecretManager()
        self.user_mgr = UserManager()
        self.app_mgr = AppManager()
        self.rb_mgr = RoleBindingManager()
        self.role_mgr = RoleManager()
        self.project_mgr = ProjectManager()
        self.project_group_mgr = ProjectGroupManager()
        self.workspace_mgr = WorkspaceManager()

    @transaction()
    @convert_model
    def issue(self, params: TokenIssueRequest) -> Union[TokenResponse, dict]:
        """Issue token
        Args:
            params (dict): {
                'credentials': 'dict',  # required
                'auth_type': 'str',     # required
                'timeout': 'int',
                'verify_code': 'str',
                'domain_id': 'str',     # required
            }
        Returns:
            TokenResponse:
        """

        domain_id = params.domain_id
        timeout = params.timeout
        verify_code = params.verify_code
        credentials = params.credentials

        private_jwk = self.domain_secret_mgr.get_domain_private_key(domain_id=domain_id)
        refresh_private_jwk = self.domain_secret_mgr.get_domain_refresh_private_key(
            domain_id=domain_id
        )

        # Check Domain state is ENABLED
        self._check_domain_state(domain_id)

        token_mgr = TokenManager.get_token_manager_by_auth_type(params.auth_type)
        token_mgr.authenticate(
            domain_id, verify_code=verify_code, credentials=credentials
        )

        user_vo = token_mgr.user
        user_mfa = user_vo.mfa.to_dict() if user_vo.mfa else {}
        permissions = self._get_permissions_from_required_actions(user_vo)

        if user_mfa.get("state", "DISABLED") == "ENABLED" and params.auth_type != "MFA":
            mfa_manager = MFAManager.get_manager_by_mfa_type(user_mfa.get("mfa_type"))
            mfa_email = user_mfa["options"].get("email")
            mfa_manager.send_mfa_authentication_email(
                user_vo.user_id, domain_id, mfa_email, user_vo.language, credentials
            )
            raise ERROR_MFA_REQUIRED(user_id=mfa_email)

        token_info = token_mgr.issue_token(
            private_jwk,
            refresh_private_jwk,
            domain_id,
            timeout=timeout,
            permissions=permissions,
        )

        return TokenResponse(**token_info)

    @transaction()
    @convert_model
    def grant(self, params: TokenGrantRequest) -> Union[GrantTokenResponse, dict]:
        """Grant token
        Args:
            params (dict): {
                'grant_type': 'str',    # required
                'token': 'str',         # required
                'scope': 'str',         # required
                'timeout': 'int',
                'workspace_id': 'str',
                'permissions': 'list',
            }
        Returns:
            GrantTokenResponse:
        """
        domain_id = self._extract_domain_id(params.token)
        timeout = params.timeout
        public_jwk = None  # todo: remove

        refresh_public_jwk = self.domain_secret_mgr.get_domain_refresh_public_key(
            domain_id=domain_id
        )

        # todo: remove
        if (
            domain_id == SystemManager.get_root_domain_id()
            and params.scope == "WORKSPACE"
        ):
            public_jwk = self.domain_secret_mgr.get_domain_public_key(domain_id)
            domain_id = params.domain_id

        if domain_id == SystemManager.get_root_domain_id() and params.scope != "SYSTEM":
            raise ERROR_PERMISSION_DENIED()
        elif params.scope == "WORKSPACE":
            if params.workspace_id is None:
                raise ERROR_REQUIRED_PARAMETER(key="workspace_id")

            self._check_workspace_state(params.workspace_id, domain_id)
            workspace_vo = self.workspace_mgr.get_workspace(
                params.workspace_id, domain_id
            )
            if workspace_vo.state != "ENABLED":
                raise ERROR_PERMISSION_DENIED()
        else:
            params.workspace_id = None

        # Check Domain state is ENABLED
        self._check_domain_state(domain_id)

        if public_jwk:
            # todo: remove
            decoded_token_info = self._verify_token(
                params.grant_type, params.token, public_jwk
            )
            role_id = "managed-workspace-owner"
            role_type = "WORKSPACE_OWNER"
            user_vo = None
        else:
            decoded_token_info = self._verify_token(
                params.grant_type, params.token, refresh_public_jwk
            )

            if decoded_token_info["owner_type"] != "USER":
                raise ERROR_PERMISSION_DENIED()

            user_vo = self.user_mgr.get_user(
                user_id=decoded_token_info["user_id"], domain_id=domain_id
            )

            self._check_user_required_actions(user_vo.required_actions, user_vo.user_id)

            role_type, role_id = self._get_user_role_info(
                user_vo, workspace_id=params.workspace_id
            )

        decoded_token_info["scope"] = params.scope
        decoded_token_info["workspace_id"] = params.workspace_id

        private_jwk = self.domain_secret_mgr.get_domain_private_key(domain_id=domain_id)
        refresh_private_jwk = self.domain_secret_mgr.get_domain_refresh_private_key(
            domain_id=domain_id
        )

        token_mgr = TokenManager.get_token_manager_by_auth_type("GRANT")
        app_id = None
        if public_jwk:
            # todo : remove
            token_mgr.is_authenticated = True
            token_mgr.owner_type = decoded_token_info.get("owner_type")
            app_id = decoded_token_info.get("app_id")
            token_mgr.role_type = role_type
        else:
            token_mgr.authenticate(
                domain_id,
                scope=params.scope,
                role_type=role_type,
                user_vo=user_vo,
            )

        if params.grant_type == "SYSTEM_TOKEN" and params.scope == "WORKSPACE":
            # todo : remove
            permissions = params.permissions
        # TODO: change name
        elif role_id == "combined-role":
            user_id = user_vo.user_id
            permissions = self._get_combined_role_permissions(
                role_type, user_id, domain_id
            )

        elif role_id:
            permissions = self._get_role_permissions(role_id, domain_id)
        else:
            permissions = None

        if role_type == "WORKSPACE_MEMBER":
            user_projects = []
            project_groups = self.project_group_mgr.filter_project_groups(
                domain_id=domain_id,
                workspace_id=params.workspace_id,
                users=user_vo.user_id,
            )

            for project_group in project_groups:
                project_group_id = project_group.project_group_id
                user_projects.extend(
                    self.project_group_mgr.get_projects_in_project_groups(
                        domain_id, project_group_id
                    )
                )

            user_projects.extend(
                self._get_user_projects(user_vo.user_id, params.workspace_id, domain_id)
            )

            user_projects = list(set(user_projects))
        else:
            user_projects = None

        token_info = token_mgr.issue_token(
            private_jwk,
            refresh_private_jwk,
            domain_id,
            timeout=timeout,
            workspace_id=params.workspace_id,
            permissions=permissions,
            projects=user_projects,
            app_id=app_id,  # todo : remove
        )

        response = {
            "access_token": token_info["access_token"],
            "role_type": role_type,
            "role_id": role_id,
            "domain_id": domain_id,
            "workspace_id": params.workspace_id,
        }

        return GrantTokenResponse(**response)

    @cache.cacheable(
        key="identity:workspace-state:{domain_id}:{workspace_id}", expire=600
    )
    def _check_workspace_state(self, workspace_id: str, domain_id: str) -> None:
        workspace_vo = self.workspace_mgr.get_workspace(workspace_id, domain_id)

        if workspace_vo.state != "ENABLED":
            raise ERROR_WORKSPACE_STATE(workspace_id=workspace_id)

    @cache.cacheable(key="identity:domain-state:{domain_id}", expire=600)
    def _check_domain_state(self, domain_id: str) -> None:
        domain_vo = self.domain_mgr.get_domain(domain_id)

        if domain_vo.state != "ENABLED":
            raise ERROR_DOMAIN_STATE(domain_id=domain_vo.domain_id)

    @staticmethod
    def _get_permissions_from_required_actions(user_vo: User) -> Union[List[str], None]:
        if "UPDATE_PASSWORD" in user_vo.required_actions:
            return [
                "identity:UserProfile",
            ]

        return None

    @staticmethod
    def _extract_domain_id(token: str) -> str:
        try:
            decoded = JWTUtil.unverified_decode(token)
        except Exception as e:
            _LOGGER.error(f"[_extract_token] {e}")
            _LOGGER.error(token)
            raise ERROR_AUTHENTICATE_FAILURE(message="Cannot decode token.")

        domain_id = decoded.get("did")

        if domain_id is None:
            raise ERROR_AUTHENTICATE_FAILURE(message="Empty domain_id provided.")

        return domain_id

    @staticmethod
    def _verify_token(grant_type: str, token: str, public_jwk: dict) -> dict:
        try:
            decoded = JWTAuthenticator(public_jwk).validate(token)
        except Exception as e:
            _LOGGER.error(f"[_verify_refresh_token] {e}")
            raise ERROR_AUTHENTICATE_FAILURE(message="Token validation failed.")

        if decoded.get("typ") != grant_type:
            raise ERROR_INVALID_GRANT_TYPE(grant_type=grant_type)

        token_info = {
            "owner_type": decoded["own"],
            "token_id": decoded["jti"],
        }

        if token_info["owner_type"] == "USER":
            token_info["user_id"] = decoded["aud"]
        else:
            token_info["app_id"] = decoded["aud"]

        return token_info

    def _get_user_role_info(
        self, user_vo: User, workspace_id: str = None
    ) -> Tuple[str, Union[str, None]]:
        if user_vo.role_type == "DOMAIN_ADMIN":
            rb_vos = self.rb_mgr.filter_role_bindings(
                user_id=user_vo.user_id,
                domain_id=user_vo.domain_id,
                role_type=user_vo.role_type,
            )

            if rb_vos.count() > 0:
                return rb_vos[0].role_type, rb_vos[0].role_id

        else:
            rb_vos = self.rb_mgr.filter_role_bindings(
                user_id=user_vo.user_id,
                domain_id=user_vo.domain_id,
                role_type=["WORKSPACE_OWNER", "WORKSPACE_MEMBER"],
                workspace_id=workspace_id,
            )

            # TODO: Check if this is correct
            if rb_vos.count() == 1:
                return rb_vos[0].role_type, rb_vos[0].role_id
            else:
                role_types = [rb.role_type for rb in rb_vos]
                if "WORKSPACE_OWNER" in role_types:
                    return "WORKSPACE_OWNER", "combined-role"
                else:
                    return "WORKSPACE_MEMBER", "combined-role"

        return "USER", None

    @staticmethod
    def _get_app_role_info(app_vo: App) -> Tuple[str, str]:
        return app_vo.role_type, app_vo.role_id

    @cache.cacheable(key="identity:role-permissions:{domain_id}:{role_id}", expire=600)
    def _get_role_permissions(self, role_id: str, domain_id: str) -> List[str]:
        role_vo = self.role_mgr.get_role(role_id=role_id, domain_id=domain_id)
        return role_vo.permissions

    def _get_user_projects(
        self, user_id: str, workspace_id: str, domain_id: str
    ) -> List[str]:
        user_projects = []

        public_project_vos = self.project_mgr.filter_projects(
            project_type="PUBLIC",
            domain_id=domain_id,
            workspace_id=workspace_id,
        )
        user_projects.extend(
            [project_vo.project_id for project_vo in public_project_vos]
        )

        user_project_vos = self.project_mgr.filter_projects(
            project_type="PRIVATE",
            domain_id=domain_id,
            users=user_id,
            workspace_id=workspace_id,
        )
        user_projects.extend([project_vo.project_id for project_vo in user_project_vos])

        return user_projects

    @staticmethod
    def _check_user_required_actions(required_actions: list, user_id: str) -> None:
        if required_actions:
            for required_action in required_actions:
                if required_action == "UPDATE_PASSWORD":
                    raise ERROR_UPDATE_PASSWORD_REQUIRED(user_id=user_id)

    def _get_combined_role_permissions(
        self, role_type: str, user_id: str, domain_id: str
    ) -> Union[List[str], None]:
        role_bindings = self.rb_mgr.filter_role_bindings(
            role_type=role_type,
            user_id=user_id,
            domain_id=domain_id,
        )
        role_ids = [rb.role_id for rb in role_bindings]

        role_infos = self.role_mgr.filter_roles(
            role_type=role_type, role_id=role_ids, domain_id=domain_id
        )

        combined_permissions = []
        for role_info in role_infos:
            if not role_info["permissions"]:
                return None

            combined_permissions.extend(role_info["permissions"])

        return list(set(combined_permissions))
