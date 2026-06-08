from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings

from app.core.database import get_db
from app.api.deps import get_current_user, require_roles
from app.schemas.subscription import SubscriptionOut, RazorpayOrderOut, VerifyPaymentIn
from app.services.subscription_service import get_or_create_subscription
from app.services.razorpay_service import create_order, verify_payment_signature
from app.services.notification_service import create_notification
from app.repositories import subscription_repository as repo

router = APIRouter(prefix="/billing", tags=["Billing"])

PLAN_CONFIG = {
    "basic": {
        "amount": 0,
        "credits": 50,
        "max_users": 5,
        "max_storage_mb": 100,
    },
    "silver": {
        "amount": 49900,
        "credits": 500,
        "max_users": 25,
        "max_storage_mb": 1024,
    },
    "gold": {
        "amount": 99900,
        "credits": 1500,
        "max_users": 100,
        "max_storage_mb": 5120,
    },
}

@router.get("/me", response_model=SubscriptionOut)
def billing_me(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not user.organization_id:
        raise HTTPException(status_code=403, detail="User is not linked to an organization")

    return get_or_create_subscription(db, user.organization_id)


@router.post("/checkout/{plan}", response_model=RazorpayOrderOut | SubscriptionOut)
def checkout_plan(
    plan: str,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    if not user.organization_id:
        raise HTTPException(status_code=403, detail="User is not linked to an organization")

    if plan not in PLAN_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid plan")

    sub = get_or_create_subscription(db, user.organization_id)

    if plan == "basic":
        sub.plan = "basic"
        sub.status = "active"
        sub.amount = 0
        sub.credits = PLAN_CONFIG[plan]["credits"]
        sub.max_users = PLAN_CONFIG[plan]["max_users"]
        sub.max_storage_mb = PLAN_CONFIG[plan]["max_storage_mb"]

        updated_sub = repo.update_subscription(db, sub)

        create_notification(
            db=db,
            user_id=user.id,
            title="Subscription updated",
            message=f"Organization subscription changed to Basic plan",
            category="billing",
        )

        return updated_sub

    order = create_order(PLAN_CONFIG[plan]["amount"])

    sub.plan = plan
    sub.status = "created"
    sub.amount = PLAN_CONFIG[plan]["amount"]
    sub.credits = PLAN_CONFIG[plan]["credits"]
    sub.max_users = PLAN_CONFIG[plan]["max_users"]
    sub.max_storage_mb = PLAN_CONFIG[plan]["max_storage_mb"]
    sub.razorpay_order_id = order["id"]
    
    updated_repo = repo.update_subscription(db, sub)

    create_notification(
        db=db,
        user_id=user.id,
        title="Subscription upgraded",
        message=f"Organization upgraded to {updated_sub.plan.title()} plan.",
        category="billing",
    )

    return updated_sub


@router.post("/verify-payment", response_model=SubscriptionOut)
def verify_payment(
    payload: VerifyPaymentIn,
    db: Session = Depends(get_db),
    user=Depends(require_roles("admin")),
):
    if not user.organization_id:
        raise HTTPException(status_code=403, detail="User is not linked to an organization")

    sub = get_or_create_subscription(db, user.organization_id)

    if sub.razorpay_order_id != payload.razorpay_order_id:
        raise HTTPException(status_code=400, detail="Order mismatch")

    if not verify_payment_signature(
        payload.razorpay_order_id,
        payload.razorpay_payment_id,
        payload.razorpay_signature,
    ):
        sub.status = "payment_failed"
        repo.update_subscription(db, sub)
        raise HTTPException(status_code=400, detail="Payment verification failed")

    sub.status = "active"
    sub.razorpay_payment_id = payload.razorpay_payment_id

    return repo.update_subscription(db, sub)

