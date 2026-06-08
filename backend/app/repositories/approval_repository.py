from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.approval import ApprovalRequest, ApprovalHistory
from app.utils.db_exceptions import handle_db_commit


def get_request_by_id(db: Session, request_id: int):
    return db.execute(
        select(ApprovalRequest).where(ApprovalRequest.id == request_id)
    ).scalar_one_or_none()


def create_request(db: Session, request: ApprovalRequest):
    db.add(request)
    handle_db_commit(db)
    db.refresh(request)
    return request


def add_history(db: Session, history: ApprovalHistory):
    db.add(history)
    db.flush()
    db.refresh(history)
    return(history)


def update_request(db: Session, request: ApprovalRequest):
    handle_db_commit(db)
    db.refresh(request)
    return(request)


def list_requests_by_organization(db: Session, organization_id: int):
    stmt = (
        select(ApprovalRequest)
        .where(ApprovalRequest.organization_id == organization_id)
        .order_by(ApprovalRequest.id.desc())
    )
    return paginate(db, stmt)


def list_requests_by_user(db: Session, user_id: int, organization_id: int):
    stmt = (
        select(ApprovalRequest)
        .where(
            ApprovalRequest.submitted_by == user_id,
            ApprovalRequest.organization_id == organization_id,
        )
        .order_by(ApprovalRequest.id.desc())
        )
    return paginate(db, stmt)

def list_requests_by_manager(db: Session, organization_id: int):
    stmt = (
        select(ApprovalRequest)
        .where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.status.in_(["pending_manager", "on_hold", "approved", "rejected"]),
        )
        .order_by(ApprovalRequest.id.desc())
        )
    return paginate(db, stmt)


def get_history_by_request(db: Session, request_id: int):
    return db.execute(
        select(ApprovalHistory).where(ApprovalHistory.approval_request_id == request_id)
    ).scalars().all()
