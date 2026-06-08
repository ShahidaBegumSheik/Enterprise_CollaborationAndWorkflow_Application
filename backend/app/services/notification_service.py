import asyncio

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories import notification_repository as repo
from app.websockets.connection_manager import manager


def send_ws_notification(user_id: int, payload: dict):
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(manager.send_to_user(user_id, payload))
    except RuntimeError:
        pass


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    category: str = "general",
):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        category=category,
        is_read=False,
    )

    saved = repo.create_notification(db, notification)

    send_ws_notification(
        user_id,
        {
            "id": saved.id,
            "type": "NOTIFICATION",
            "title": saved.title,
            "message": saved.message,
            "category": saved.category,
            "created_at": str(saved.created_at),
        },
    )

    return saved


def list_my_notifications_service(db: Session, user):
    return repo.list_user_notifications(db, user.id)


def get_unread_count_service(db, user):
    return {
        "unread_count": repo.count_unread_notifications(db, user.id)
    }


def mark_notification_read_service(db: Session, notification_id: int, user):
    notification = repo.mark_notification_read(db, notification_id, user.id)

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return notification


def mark_all_notifications_read_service(db: Session, user):
    return repo.mark_all_read(db, user.id)

