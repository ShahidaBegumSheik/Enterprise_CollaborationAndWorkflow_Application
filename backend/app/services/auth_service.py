import secrets
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.models.user import User
from app.models.password_reset import PasswordResetToken
from app.repositories.user_repository import get_user_by_email, create_user, update_user
from app.repositories.password_reset_repository import (
    create_reset_token,
    get_reset_token,
    update_reset_token,
)
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas.user import UserOut
from app.core.logger import logger


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
    
    logger.info(f"Login successful for {payload.email}")

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user).model_dump(),
    }

def forgot_password_service(db, payload):
    user = get_user_by_email(db, payload.email)

    if not user:
        return {"message": "If email exist, reset token has been generated"}
    
    token = secrets.token_urlsafe(32)

    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=30),
        used=False,
    )

    create_reset_token(db, reset_token)

    return {
        "message": "Password reset token generated",
        "reset_token": token,
    }

def reset_password_service(db, payload):
    reset_token = get_reset_token(db, payload.token)

    if not reset_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset token")
    
    if reset_token.used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token already used")
    
    if reset_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expired")
    
    user = db.get(User, reset_token.user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user.password_hash = hash_password(payload.new_password)
    reset_token.used = True

    update_user(db, user)
    update_reset_token(db, reset_token)

    return {"message": "Password reset successfully"}
