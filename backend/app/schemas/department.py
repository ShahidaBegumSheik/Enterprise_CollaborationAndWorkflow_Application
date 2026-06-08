from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    name: str
    description: str | None = None

class DepartmentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class DepartmentOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)