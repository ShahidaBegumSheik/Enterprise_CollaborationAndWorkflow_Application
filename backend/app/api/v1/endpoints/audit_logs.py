from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import require_roles
from app.services.audit_service import list_audit_logs_service

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])


@router.get("")
def list_audit_logs(db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return list_audit_logs_service(db)
