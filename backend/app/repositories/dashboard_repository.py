from sqlalchemy import select, func, or_
from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.user import User
from app.models.document import Document
from app.models.approval import ApprovalRequest


def count_tasks_by_filter(db: Session, task_filter):
    total_tasks = db.execute(
        select(func.count(Task.id)).where(task_filter)
    ).scalar() or 0

    done_tasks = db.execute(
        select(func.count(Task.id)).where(task_filter, Task.status == "done")
    ).scalar() or 0

    todo_tasks = db.execute(
        select(func.count(Task.id)).where(task_filter, Task.status == "todo")
    ).scalar() or 0

    in_progress_tasks = db.execute(
        select(func.count(Task.id)).where(task_filter, Task.status == "in_progress")
    ).scalar() or 0

    review_tasks = db.execute(
        select(func.count(Task.id)).where(task_filter, Task.status == "review")
    ).scalar() or 0

    return {
        "total_tasks": total_tasks,
        "done_tasks": done_tasks,
        "completed_tasks": done_tasks,
        "pending_tasks": total_tasks - done_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "review_tasks": review_tasks,
    }


def get_employee_task_summary(db: Session, organization_id: int, user_id: int):
    return count_tasks_by_filter(
        db,
        (Task.organization_id == organization_id) & (Task.assignee_id == user_id),
    )


def get_manager_task_summary(db: Session, organization_id: int, user_id: int):
    return count_tasks_by_filter(
        db,
        (Task.organization_id == organization_id)
        & ((Task.created_by == user_id) | (Task.assignee_id == user_id)),
    )


def get_admin_task_summary(db: Session, organization_id: int):
    return count_tasks_by_filter(
        db,
        Task.organization_id == organization_id,
    )


def count_employee_requests(db: Session, organization_id: int, user_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.submitted_by == user_id,
        )
    ).scalar() or 0


def count_employee_pending_requests(db: Session, organization_id: int, user_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.submitted_by == user_id,
            ApprovalRequest.status.in_(["pending_manager", "pending_admin", "on_hold"]),
        )
    ).scalar() or 0


def count_employee_approved_requests(db: Session, organization_id: int, user_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.submitted_by == user_id,
            ApprovalRequest.status == "approved",
        )
    ).scalar() or 0


def count_manager_pending_approvals(db: Session, organization_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.status == "pending_manager",
        )
    ).scalar() or 0


def count_on_hold_approvals(db: Session, organization_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.status == "on_hold",
        )
    ).scalar() or 0


def count_transferred_to_admin(db: Session, organization_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id,
            ApprovalRequest.status == "pending_admin",
        )
    ).scalar() or 0


def count_users_by_organization(db: Session, organization_id: int):
    return db.execute(
        select(func.count(User.id)).where(User.organization_id == organization_id)
    ).scalar() or 0


def count_documents_by_organization(db: Session, organization_id: int):
    return db.execute(
        select(func.count(Document.id)).where(Document.organization_id == organization_id)
    ).scalar() or 0


def count_approvals_by_organization(db: Session, organization_id: int):
    return db.execute(
        select(func.count(ApprovalRequest.id)).where(
            ApprovalRequest.organization_id == organization_id
        )
    ).scalar() or 0

