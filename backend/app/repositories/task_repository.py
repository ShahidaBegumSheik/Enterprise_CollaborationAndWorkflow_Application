from sqlalchemy import select, or_
from sqlalchemy.orm import Session, selectinload
from app.models.task import Task
from app.utils.db_exceptions import handle_db_commit

from fastapi_pagination.ext.sqlalchemy import paginate


def get_task_by_id_and_organization(
    db: Session,
    task_id: int,
    organization_id: int,
):
    stmt = (
        select(Task)
        .where(
            Task.id == task_id,
            Task.organization_id == organization_id,
        )
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator),
        )
    )

    return db.execute(stmt).scalar_one_or_none()


def list_tasks_for_employee(db: Session, user_id: int, organization_id: int):
    stmt = (select(Task)
            .where(
                Task.organization_id == organization_id,
                or_(
                    Task.assignee_id == user_id,
                    Task.created_by == user_id,
                ),                
            )
            .options(
                selectinload(Task.assignee),
                selectinload(Task.creator),
            )
            .order_by(Task.id.desc())
    )
    return paginate(db, stmt)


def list_tasks_for_manager(db: Session, user_id: int, organization_id: int):
    stmt = (select(Task)
            .where(
                Task.organization_id == organization_id,
                (Task.created_by == user_id) | (Task.assignee_id == user_id),
            )
            .options(
                selectinload(Task.assignee),
                selectinload(Task.creator)
            )
            .order_by(Task.id.desc())
    )
    return paginate(db, stmt)


def list_tasks_by_organization(db: Session, organization_id: int):
    stmt = (
        select(Task)
        .where(Task.organization_id == organization_id)
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
        .order_by(Task.id.desc())
    )
    return paginate(db, stmt)


def create_task(db: Session, task: Task):
    db.add(task)
    handle_db_commit(db)
    db.refresh(task)
    return task

def update_task(db: Session, task: Task):
    handle_db_commit(db)
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    handle_db_commit(db)

