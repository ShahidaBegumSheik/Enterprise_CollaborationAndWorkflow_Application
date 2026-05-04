from sqlalchemy import select
from app.models.audit_log import AuditLog

def create_log(db, log):
    db.add(log)
    db.commit()

def list_logs(db):
    return db.execute(select(AuditLog)).scalars().all()