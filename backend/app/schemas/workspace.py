from pydantic import BaseModel, ConfigDict

class WorkspaceCreate(BaseModel):
    name: str
    description: str | None = None
    department_id: int | None = None

class WorkspaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    department_id: int | None = None

class WorkspaceOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    department_id: int | None = None

    model_config = ConfigDict(from_attributes=True)