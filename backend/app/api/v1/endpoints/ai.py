from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import require_roles
from app.services.ai_service import (
    get_ai_task_insights_service,
    recommend_assignee_service,
)
from app.services.subscription_service import deduct_credit

router = APIRouter(prefix="/ai", tags=["AI Insights"])


@router.get("/task-insights")
def task_insights(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    deduct_credit(db, current_user.organization_id, 1)
    return get_ai_task_insights_service(db, current_user)


@router.get("/recommend-assignee")
def recommend_assignee(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager")),
):
    deduct_credit(db, current_user.organization_id, 1)
    return recommend_assignee_service(db, current_user)
