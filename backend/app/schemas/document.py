from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DocumentOut(BaseModel):
    id: int
    original_name: str
    stored_name: str
    file_path: str
    version: int
    task_id: int | None = None
    approval_request_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)