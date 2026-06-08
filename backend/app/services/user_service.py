from fastapi import HTTPException, status
from sqlalchemy import select, func
from app.models.user import User
from app.core.security import hash_password
from app.repositories import user_repository as repo
from app.services.subscription_service import get_or_create_subscription
from app.services.notification_service import create_notification

def list_users_service(db, current_user):
    return repo.list_users_by_organization(db, current_user.organization_id)


def create_user_service(db, payload, current_user):
    if not current_user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Current user is not linked to an organization")
    
    existing_user = repo.get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    subscription = get_or_create_subscription(
        db,
        current_user.organization_id
    )

    current_user_count = repo.count_users_by_organization(
        db,
        current_user.organization_id
    )

    if current_user_count >= subscription.max_users:
        raise HTTPException(
            status_code=403,
            detail="User limit reached. Please upgrade your subscription."
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department_id=payload.department_id,
        organization_id=current_user.organization_id,
    )

    current_user = repo.create_user(db, user)

    create_notification(
        db=db,
        user_id=user.id,
        title="Welcome",
        message=f"Your account has been created successfully",
        category="user",
    )

    return current_user


def update_user_service(db, user_id: int, payload):
    user = repo.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)

    old_role = user.role

    for field, value in update_data.items():
        if field == "password":
            user.password_hash = hash_password(value)
        else:
            setattr(user, field, value)

    updated_user = repo.update_user(db, user)

    if "role" in update_data and update_data["role"] != old_role:
        create_notification(
            db=db,
            user_id=updated_user.id,
            title="Role updated",
            message=f"Your role has been changed to {updated_user.role}.",
            category="user",
        )
        
        return updated_user


def delete_user_service(db, user_id: int):
    user = repo.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    repo.delete_user(db, user)

    return {"message": "User deleted successfully"}


def list_valid_task_assignees_service(db, current_user):
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to an organization",
        )

    role = str(current_user.role).lower()

    if role == "admin":
        allowed_roles = ["manager", "employee"]

    elif role == "manager":
        allowed_roles = ["employee"]

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employees cannot assign tasks",
        )

    return repo.list_valid_task_assignees(
        db=db,
        organization_id=current_user.organization_id,
        current_user_id=current_user.id,
        allowed_roles=allowed_roles,
    )

