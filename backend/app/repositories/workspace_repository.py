from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.workspace import Workspace
from app.utils.db_exceptions import handle_db_commit

def list_workspaces(db: Session):
    stmt = select(Workspace).order_by(Workspace.id.desc())
    return paginate(db, stmt)

def get_workspace_by_id(db: Session, workspace_id: int):
    stmt = select(Workspace).where(Workspace.id == workspace_id)
    return db.execute(stmt).scalar_one_or_none()

def create_workspace(db: Session, workspace: Workspace):
    db.add(workspace)
    handle_db_commit(db)
    db.refresh(workspace)
    return workspace

def update_workspace(db: Session, workspace: Workspace):
    handle_db_commit(db)
    db.refresh(workspace)
    return workspace

def delete_workspace(db: Session, workspace: Workspace):
    db.delete(workspace)
    handle_db_commit(db)
