from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.approval import ApprovalCreate, ApprovalAction, ApprovalOut
from app.services.approval_service import (
    create_request_service,
    list_requests_service,
    approval_action_service,
    get_approval_history_service,
)
from fastapi_pagination import Page

router = APIRouter(prefix="/approvals", tags=["Approvals"])


@router.post("")
async def create_request(
    payload: ApprovalCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return await create_request_service(db, payload, user)


@router.get("", response_model=Page[ApprovalOut])
def list_requests(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return list_requests_service(db, user)


@router.post("/{id}/action")
def action(
    id: int,
    payload: ApprovalAction,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return approval_action_service(db, id, payload, user)


@router.get("/{id}/history")
def history(
    id: int,
    db: Session = Depends(get_db),
):
    return get_approval_history_service(db, id)

