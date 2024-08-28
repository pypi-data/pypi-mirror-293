import logging
from typing import Tuple
from mongoengine import QuerySet

from spaceone.core import cache
from spaceone.core.manager import BaseManager

from spaceone.identity.manager.role_binding_manager import RoleBindingManager
from spaceone.identity.model.workspace.database import Workspace

_LOGGER = logging.getLogger(__name__)


class WorkspaceManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workspace_model = Workspace

    def create_workspace(self, params: dict) -> Workspace:
        def _rollback(vo: Workspace):
            _LOGGER.info(
                f"[create_workspace._rollback] Delete workspace : {vo.name} ({vo.workspace_id}) ({vo.domain_id})"
            )
            vo.delete()

        params["dormant_ttl"] = -1
        params["service_account_count"] = 0
        params["cost_info"] = {
            "day": 0,
            "month": 0,
        }

        workspace_vo = self.workspace_model.create(params)
        self.transaction.add_rollback(_rollback, workspace_vo)

        return workspace_vo

    def update_workspace_by_vo(
        self, params: dict, workspace_vo: Workspace
    ) -> Workspace:
        def _rollback(old_data):
            _LOGGER.info(
                f'[update_workspace._rollback] Revert Data : {old_data["name"]} ({old_data["workspace_id"]})'
            )
            workspace_vo.update(old_data)

        self.transaction.add_rollback(_rollback, workspace_vo.to_dict())

        return workspace_vo.update(params)

    @staticmethod
    def delete_workspace_by_vo(workspace_vo: Workspace) -> None:
        rb_mgr = RoleBindingManager()
        rb_vos = rb_mgr.filter_role_bindings(
            workspace_id=workspace_vo.workspace_id, domain_id=workspace_vo.domain_id
        )

        if rb_vos.count() > 0:
            _LOGGER.debug(
                f"[delete_workspace_by_vo] Delete role bindings count with {workspace_vo.workspace_id} : {rb_vos.count()}"
            )
            rb_vos.delete()

        workspace_vo.delete()

        cache.delete_pattern(
            f"identity:workspace-state:{workspace_vo.domain_id}:{workspace_vo.workspace_id}"
        )

    def enable_workspace(self, workspace_vo: Workspace) -> Workspace:
        self.update_workspace_by_vo({"state": "ENABLED"}, workspace_vo)
        cache.delete_pattern(
            f"identity:workspace-state:{workspace_vo.domain_id}:{workspace_vo.workspace_id}"
        )

        return workspace_vo

    def disable_workspace(self, workspace_vo: Workspace) -> Workspace:
        self.update_workspace_by_vo({"state": "DISABLED"}, workspace_vo)
        cache.delete_pattern(
            f"identity:workspace-state:{workspace_vo.domain_id}:{workspace_vo.workspace_id}"
        )

        return workspace_vo

    def get_workspace(self, workspace_id: str, domain_id: str) -> Workspace:
        return self.workspace_model.get(domain_id=domain_id, workspace_id=workspace_id)

    def filter_workspaces(self, **conditions) -> QuerySet:
        return self.workspace_model.filter(**conditions)

    def list_workspaces(self, query: dict) -> Tuple[QuerySet, int]:
        return self.workspace_model.query(**query)

    def stat_workspaces(self, query: dict) -> dict:
        return self.workspace_model.stat(**query)
