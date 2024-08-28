from typing import Union, Literal
from pydantic import BaseModel

__all__ = [
    "WorkspaceCreateRequest",
    "WorkspaceUpdateRequest",
    "WorkspaceDeleteRequest",
    "WorkspaceEnableRequest",
    "WorkspaceDisableRequest",
    "WorkspaceGetRequest",
    "WorkspaceCheckRequest",
    "WorkspaceSearchQueryRequest",
    "WorkspaceStatQueryRequest",
    "State",
]

State = Literal["ENABLED", "DISABLED"]


class WorkspaceCreateRequest(BaseModel):
    name: str
    tags: Union[dict, None] = None
    domain_id: str


class WorkspaceUpdateRequest(BaseModel):
    workspace_id: str
    name: Union[str, None] = None
    tags: Union[dict, None] = None
    domain_id: str


class WorkspaceDeleteRequest(BaseModel):
    force: Union[bool, None] = False
    workspace_id: str
    domain_id: str


class WorkspaceEnableRequest(BaseModel):
    workspace_id: str
    domain_id: str


class WorkspaceDisableRequest(BaseModel):
    workspace_id: str
    domain_id: str


class WorkspaceGetRequest(BaseModel):
    workspace_id: str
    domain_id: str


class WorkspaceCheckRequest(BaseModel):
    workspace_id: str
    domain_id: str


class WorkspaceSearchQueryRequest(BaseModel):
    query: Union[dict, None] = None
    name: Union[str, None] = None
    state: Union[State, None] = None
    workspace_id: Union[str, None] = None
    created_by: Union[str, None] = None
    is_managed: Union[bool, None] = None
    is_dormant: Union[bool, None] = None
    domain_id: str


class WorkspaceStatQueryRequest(BaseModel):
    query: dict
    domain_id: str
