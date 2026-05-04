from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_roles
from app.services.user_service import *
from app.schemas.user import UserOut, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "employee"))
):
    return list_users_service(db)


@router.post("/")
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    return create_user_service(db, payload)


@router.put("/{user_id}")
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    return update_user_service(db, user_id, payload)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot delete your own account")
    
    return delete_user_service(db, user_id)

