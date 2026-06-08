from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User

def list_pending_tasks_by_organization(db: Session, organization_id: int):
    stmt = (
        select(Task)
        .where(
            Task.organization_id == organization_id,
            Task.status != "done",
        )
        .order_by(Task.due_date.asc())
    )
    return db.execute(stmt).scalars().all()


def list_active_employees_by_organization(db: Session, organization_id: int):
    stmt = select(User).where(
        User.organization_id == organization_id,
        User.role == "employee",
        User.is_active == True,
    )
    return db.execute(stmt).scalars().all()


def count_pending_tasks_for_user(db: Session, user_id: int, organization_id: int):
    stmt = select(func.count(Task.id)).where(
        Task.organization_id == organization_id,
        Task.assignee_id == user_id,
        Task.status != "done",
    )
    return db.execute(stmt).scalar() or 0


def count_completed_tasks_for_user(db: Session, user_id: int, organization_id: int):
    stmt = select(func.count(Task.id)).where(
        Task.organization_id == organization_id,
        Task.assignee_id == user_id,
        Task.status == "done",
    )
    return db.execute(stmt).scalar() or 0


def count_overdue_tasks_for_user(db: Session, user_id: int, organization_id: int):
    stmt = select(func.count(Task.id)).where(
        Task.organization_id == organization_id,
        Task.assignee_id == user_id,
        Task.status != "done",
        Task.due_date < datetime.now(timezone.utc),
    )
    return db.execute(stmt).scalar() or 0