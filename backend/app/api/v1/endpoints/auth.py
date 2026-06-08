from fastapi import APIRouter, Depends, HTTPException, status, Request
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import LoginRequest, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth_service import (
    register_user_service,
    login_user_service,
    forgot_password_service,
    reset_password_service,
)
from app.services.google_oauth_service import get_google_auth_url, google_login_service
from app.core.security import create_access_token
from app.repositories.user_repository import get_user_by_email
from app.core.rate_limit import limiter
from app.api.deps import get_current_user
from types import SimpleNamespace

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user_service(db, payload)

@router.post("/refresh")
def refresh_token(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("refresh_token")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token required")
    
    try:
        decoded = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        
        email = decoded.get("sub")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="nvalid refresh token")
       
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return {
        "access_token": create_access_token(user.email),
        "token_type": "bearer",
    }

@router.post("/forgot-password")
def forgot_password(
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return forgot_password_service(db, payload)

@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return reset_password_service(db, payload)


@router.get("/google/login")
def google_login():
    return RedirectResponse(get_google_auth_url())


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    return await google_login_service(db, code)


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    payload = SimpleNamespace(
        email=form_data.username,
        password=form_data.password,
    )
    return login_user_service(db, payload)

@router.get("/me", response_model=UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user
