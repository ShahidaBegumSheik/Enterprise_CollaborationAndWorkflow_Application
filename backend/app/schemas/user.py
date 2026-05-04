from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: str = "employee"
    department_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: str | None = None
    department_id: int | None = None


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    department_id: int | None = None

    class Config:
        from_attributes = True
