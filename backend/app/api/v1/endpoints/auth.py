from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginRequest
from app.services.auth_service import (
    register_user_service,
    login_user_service,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user_service(db, payload)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    payload = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )
    return login_user_service(db, payload)