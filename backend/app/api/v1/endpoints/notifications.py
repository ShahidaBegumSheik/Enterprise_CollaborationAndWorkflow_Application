from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.notification import NotificationOut
from app.services.notification_service import (
    list_my_notifications_service,
    mark_notification_read_service,
    mark_all_notifications_read_service,
    get_unread_count_service,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=Page[NotificationOut])
def list_my_notifications(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return list_my_notifications_service(db, user)


@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    return get_unread_count_service(db, current_user)


@router.patch("/read-all")
def mark_all_read(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return mark_all_notifications_read_service(db, user)


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return mark_notification_read_service(db, notification_id, user)
