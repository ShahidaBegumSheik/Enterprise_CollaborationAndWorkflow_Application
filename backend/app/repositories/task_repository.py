from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models.task import Task


def get_task_by_id(db: Session, task_id: int):
    stmt = (
        select(Task)
        .where(Task.id == task_id)
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    return db.execute(stmt).scalar_one_or_none()


def list_all_tasks(db: Session):
    stmt = (select(Task)
    .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    return db.execute(stmt).scalars().all()


def list_tasks_for_employee(db: Session, user_id: int):
    stmt = (select(Task).where(Task.assignee_id == user_id)
    .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    return db.execute(stmt).scalars().all()


def list_tasks_for_manager(db: Session, user_id: int):
    stmt = (select(Task).where(
        (Task.created_by == user_id) | (Task.assignee_id == user_id))
        .options(
            selectinload(Task.assignee),
            selectinload(Task.creator)
        )
    )
    return db.execute(stmt).scalars().all()


def create_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

