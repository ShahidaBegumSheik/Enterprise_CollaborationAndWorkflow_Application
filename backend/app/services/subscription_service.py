from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.subscription import Subscription
from app.models.task import Task
from app.repositories import subscription_repository as repo

FREE_TASK_LIMIT = 50


def get_or_create_subscription(db: Session, organization_id: int) -> Subscription:
    sub = repo.get_subscription_by_organization(db, organization_id)

    if sub: 
        return sub
    
    sub = Subscription(
        organization_id=organization_id, 
        plan="basic", 
        status="active", 
        provider="razorpay",
        credits=50,
        amount=0,
    )
        
    return repo.create_subscription(db, sub)


def enforce_task_limit(db: Session, organization_id: int):
    sub = get_or_create_subscription(db, organization_id)
    
    if sub.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Subscription inactive",
        )

    if sub.plan == "basic":
        stmt = select(func.count(Task.id)).where(
            Task.organization_id == organization_id
        )

        count = db.execute(stmt).scalar() or 0

        if count >= FREE_TASK_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Free plan task limit reached ({FREE_TASK_LIMIT}). Upgrade Plan.",
            )


def deduct_credit(db: Session, organization_id: int, credits: int = 1):
    sub = get_or_create_subscription(db, organization_id)

    if sub.credits < credits:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough credits. Please upgrade your subscription.",
        )

    sub.credits -= credits
    return repo.update_subscription(db, sub)


def touch_subscription(sub: Subscription):
    sub.updated_at = datetime.now(timezone.utc)
