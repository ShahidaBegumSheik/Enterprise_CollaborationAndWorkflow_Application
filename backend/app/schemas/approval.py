from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ApprovalCreate(BaseModel):
    request_type: str
    title: str
    description: str | None = None
    amount: float | None = None


class ApprovalAction(BaseModel):
    action: str
    comment: str | None = None


class ApprovalOut(BaseModel):
    id: int
    request_type: str
    title: str
    description: str | None
    amount: int | None
    status: str
    submitted_by: int
    current_approver_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
