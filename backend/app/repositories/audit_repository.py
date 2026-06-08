from sqlalchemy import select
from app.models.audit_log import AuditLog
from app.utils.db_exceptions import handle_db_commit

from fastapi_pagination.ext.sqlalchemy import paginate

def create_log(db, log):
    db.add(log)
    handle_db_commit(db)
    db.refresh(log)
    return log

def list_logs(db):
    stmt = select(AuditLog).order_by(AuditLog.id.desc())
    return paginate(db, stmt)

def list_logs_by_entity(db, entity_type: str, entity_id: int):
    stmt = (
        select(AuditLog)
        .where(
            AuditLog.entity_type == entity_type,
            AuditLog.entity_id == entity_id,
        )
        .order_by(AuditLog.id.desc())
    )
    return db.execute(stmt).scalars().all()