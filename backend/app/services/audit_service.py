from app.models.audit_log import AuditLog
from app.repositories import audit_repository as repo


def create_audit_log(db, user_id, action, entity, entity_id, message):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity,
        entity_id=entity_id,
        details=message,
    )
    repo.create_log(db, log)


def list_audit_logs_service(db):
    return repo.list_logs(db)

def list_entity_history_service(db, entity_type: str, entity_id: int):
    return repo.list_logs_by_entity(db, entity_type, entity_id)