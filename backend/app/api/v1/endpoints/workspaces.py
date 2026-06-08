from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page

from app.core.database import get_db
from app.api.deps import require_roles
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceOut
from app.services.workspace_service import (
    list_workspace_service,
    create_workspace_service,
    update_workspace_service,
    delete_workspace_service,
)

router = APIRouter(prefix="/workspaces", tags=["workspaces"])

@router.get("", response_model=Page[WorkspaceOut])
def list_workspace(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "employee"))
):
    return list_workspace_service(db)

@router.post("", response_model=WorkspaceOut)
def create_workspace(
    payload: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return create_workspace_service(db, payload)

@router.put("/{workspace_id}", response_model=WorkspaceOut)
def update_workspace(
    workspace_id: int,
    payload: WorkspaceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    return update_workspace_service(db, workspace_id, payload)

@router.delete("/{workspace_id}")
def delete_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return delete_workspace_service(db, workspace_id)
