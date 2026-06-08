from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.notification import Notification
from app.utils.db_exceptions import handle_db_commit


def create_notification(db: Session, notification: Notification):
    db.add(notification)
    handle_db_commit(db)
    db.refresh(notification)
    return notification


def list_user_notifications(db: Session, user_id: int):
    stmt = (
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )
    return paginate(db, stmt)

def count_unread_notifications(db, user_id: int):
    stmt = select(func.count(Notification.id)).where(
        Notification.user_id == user_id,
        Notification.is_read == False,
    )
    return db.execute(stmt).scalar() or 0


def mark_notification_read(db: Session, notification_id: int, user_id: int):
    stmt = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == user_id,
    )

    notification = db.execute(stmt).scalar_one_or_none()

    if notification:
        notification.is_read = True
        handle_db_commit(db)
        db.refresh(notification)

    return notification


def mark_all_read(db: Session, user_id: int):
    stmt = (
        update(Notification)
        .where(Notification.user_id == user_id)
        .values(is_read=True)
    )

    db.execute(stmt)
    handle_db_commit(db)

    return {"message": "All notifications marked as read"}

