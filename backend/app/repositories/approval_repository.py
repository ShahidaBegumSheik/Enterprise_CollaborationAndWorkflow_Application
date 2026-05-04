from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.approval import ApprovalRequest, ApprovalHistory


def get_request_by_id(db: Session, request_id: int):
    return db.execute(
        select(ApprovalRequest).where(ApprovalRequest.id == request_id)
    ).scalar_one_or_none()


def create_request(db: Session, request: ApprovalRequest):
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


def add_history(db: Session, history: ApprovalHistory):
    db.add(history)
    db.flush()


def list_requests(db: Session):
    return db.execute(select(ApprovalRequest)).scalars().all()


def list_requests_by_user(db: Session, user_id: int):
    return db.execute(
        select(ApprovalRequest).where(ApprovalRequest.submitted_by == user_id)
    ).scalars().all()


def get_history_by_request(db: Session, request_id: int):
    return db.execute(
        select(ApprovalHistory).where(ApprovalHistory.approval_request_id == request_id)
    ).scalars().all()
