from fastapi import HTTPException, status

from app.models.workspace import Workspace
from app.repositories import workspace_repository as repo
from app.utils.sanitize import clean_text

def list_workspace_service(db):
    return repo.list_workspaces(db)


def create_workspace_service(db, payload):
    workspace = Workspace(
        name=clean_text(payload.name),
        description=clean_text(payload.description),
        department_id=payload.department_id,
    )
    return repo.create_workspace(db, workspace)

def update_workspace_service(db, workspace_id: int, payload):
    workspace = repo.get_workspace_by_id(db, workspace_id)

    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace Not Found")
    
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(workspace, field, clean_text(value) if isinstance(value, str) else value)
    
    return repo.update_workspace(db, workspace)

def delete_workspace_service(db, workspace_id: int):
    workspace = repo.get_workspace_by_id(db, workspace_id)

    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace Not Found")
    
    repo.delete_workspace(db, workspace)

    return {"message": "Workspace Deleted Successfully"}