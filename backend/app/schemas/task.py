from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"
    due_date: datetime | None = None
    assignee_id: int | None = None
    workspace_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None
    assignee_id: int | None = None
    workspace_id: int | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    due_date: datetime | None
    created_by: int
    assignee_id: int | None
    workspace_id: int | None

    creator_name: str | None = None
    assignee_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
