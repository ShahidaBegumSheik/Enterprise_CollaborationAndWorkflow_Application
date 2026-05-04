from fastapi import HTTPException
from app.models.user import User
from app.repositories.user_repository import get_user_by_email, create_user
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user import UserOut


def register_user_service(db, payload):
    existing = get_user_by_email(db, payload.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department_id=payload.department_id,
    )

    return create_user(db, user)


def login_user_service(db, payload):
    user = get_user_by_email(db, payload.email)

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user).model_dump(),
    }
