from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.utils.db_exceptions import handle_db_commit

def get_subscription_by_organization(db: Session, organization_id: int):
    stmt = select(Subscription).where(
        Subscription.organization_id == organization_id
    )

    return db.execute(stmt).scalar_one_or_none()

def get_subscription_by_order_id(db: Session, order_id: str):
    stmt = select(Subscription).where(
        Subscription.razorpay_order_id == order_id
    )

    return db.execute(stmt).scalar_one_or_none()

def create_subscription(db: Session, subscription: Subscription):
    db.add(subscription)
    handle_db_commit(db)
    db.refresh(subscription)
    return subscription

def update_subscription(db: Session, subscription: Subscription):
    handle_db_commit(db)
    db.refresh(subscription)
    return subscription