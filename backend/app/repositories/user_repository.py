from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.db_exceptions import handle_db_commit

from fastapi_pagination.ext.sqlalchemy import paginate


def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: int):
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_valid_assignee_by_id(
    db: Session,
    assignee_id: int,
    organization_id: int,
):
    stmt = (
        select(User)
        .where(
            User.id == assignee_id,
            User.organization_id == organization_id,
            User.is_active == True,
        )
    )

    return db.execute(stmt).scalar_one_or_none()


def list_admin_users_by_organization(
    db: Session,
    organization_id: int,
):
    stmt = (
        select(User)
        .where(
            User.organization_id == organization_id,
            User.role == "admin",
            User.is_active == True
        )
        .order_by(User.full_name)
    )

    return db.execute(stmt).scalars().all()

def list_manager_users_by_organization(
    db: Session,
    organization_id: int,
):
    stmt = (
        select(User)
        .where(
            User.organization_id == organization_id,
            User.role == "manager",
            User.is_active == True
        )
        .order_by(User.full_name)
    )

    return db.execute(stmt).scalars().all()


def list_users_by_organization(db: Session, organization_id: int):
    stmt = (
        select(User)
        .where(User.organization_id == organization_id)
        .order_by(User.id.desc())
    )
    return paginate(db, stmt)


def create_user(db: Session, user: User):
    db.add(user)
    handle_db_commit(db)
    db.refresh(user)
    return user


def update_user(db: Session, user: User):
    handle_db_commit(db)
    db.refresh(user)
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    handle_db_commit(db)


def count_users_by_organization(db, organization_id: int) -> int:
    return (
        db.execute(
            select(func.count(User.id))
            .where(User.organization_id == organization_id)
        ).scalar()
        or 0
    )


def list_valid_task_assignees(
    db: Session,
    organization_id: int,
    current_user_id: int,
    allowed_roles: list[str],
):
    stmt = (
        select(User)
        .where(
            User.organization_id == organization_id,
            User.id != current_user_id,
            User.role.in_(allowed_roles),
            User.is_active == True,
        )
        .order_by(User.role, User.full_name)
    )

    return db.execute(stmt).scalars().all()

