from fastapi import HTTPException

from app.models.user import User
from app.core.security import hash_password
from app.repositories import user_repository as repo


def list_users_service(db):
    return repo.list_users(db)


def create_user_service(db, payload):
    existing_user = repo.get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department_id=payload.department_id,
    )

    return repo.create_user(db, user)


def update_user_service(db, user_id: int, payload):
    user = repo.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "password":
            user.password_hash = hash_password(value)
        else:
            setattr(user, field, value)

    return repo.update_user(db, user)


def delete_user_service(db, user_id: int):
    user = repo.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    repo.delete_user(db, user)

    return {"message": "User deleted successfully"}
