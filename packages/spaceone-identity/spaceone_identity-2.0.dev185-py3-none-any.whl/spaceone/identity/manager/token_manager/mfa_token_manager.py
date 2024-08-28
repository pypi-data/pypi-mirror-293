import logging

from spaceone.identity.error.error_authentication import *
from spaceone.identity.error.error_user import *
from spaceone.identity.error.error_mfa import *
from spaceone.identity.manager.external_auth_manager import ExternalAuthManager
from spaceone.identity.manager.domain_manager import DomainManager
from spaceone.identity.manager.user_manager import UserManager
from spaceone.identity.manager.mfa_manager.base import MFAManager
from spaceone.identity.manager.token_manager.base import TokenManager
from spaceone.identity.model.domain.database import Domain
from spaceone.identity.model.user.database import User

_LOGGER = logging.getLogger(__name__)


class MFATokenManager(TokenManager):
    domain: Domain = None
    auth_type = "MFA"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain_mgr = DomainManager()
        self.external_auth_mgr = ExternalAuthManager()
        self.user_mgr = UserManager()

    def authenticate(self, domain_id: str, **kwargs):
        credentials = kwargs.get("credentials", {})
        mfa_info = MFAManager.get_mfa_info(credentials)
        if mfa_info is None:
            raise ERROR_INVALID_CREDENTIALS()

        user_id = mfa_info.get("user_id")
        domain_id = mfa_info.get("domain_id")

        self.user: User = self.user_mgr.get_user(user_id, domain_id)
        self._check_user_state()

        if verify_code := kwargs.get("verify_code"):
            if MFAManager.check_mfa_verify_code(credentials, verify_code):
                self.is_authenticated = True
            else:
                raise ERROR_INVALID_CREDENTIALS()
        else:
            user_mfa = self.user.mfa.to_dict()
            mfa_email = user_mfa["options"].get("email")

            mfa_manager = MFAManager.get_manager_by_mfa_type(user_mfa.get("mfa_type"))
            mfa_manager.send_mfa_authentication_email(
                self.user.user_id, domain_id, mfa_email, self.user.language, credentials
            )
            raise ERROR_MFA_REQUIRED(user_id=mfa_email)

    def _check_user_state(self) -> None:
        if self.user.state not in ["ENABLED", "PENDING"]:
            raise ERROR_USER_STATE_DISABLED(user_id=self.user.user_id)
        if self.user.mfa is None or self.user.mfa.state != "ENABLED":
            raise ERROR_MFA_NOT_ENABLED(key="user_id", value=self.user.user_id)
