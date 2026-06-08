from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_roles
from app.services.audit_service import list_audit_logs_service, list_entity_history_service
from app.schemas.audit_log import AuditLogOut
from fastapi_pagination import Page

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("", response_model=Page[AuditLogOut])
def list_audit_logs(db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return list_audit_logs_service(db)

@router.get("/{entity_type}/{entity_id}/history", response_model=list[AuditLogOut])
def entity_history(
    entity_type: str,
    entity_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    return list_entity_history_service(db, entity_type, entity_id)