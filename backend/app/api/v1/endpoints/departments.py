from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page

from app.core.database import get_db
from app.api.deps import require_roles
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.services.department_service import (
    list_departments_service,
    create_department_service,
    update_department_service,
    delete_department_service,
)

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.get("", response_model=Page[DepartmentOut])
def list_departments(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin", "manager", "employee"))
):
    return list_departments_service(db)

@router.post("", response_model=DepartmentOut)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return create_department_service(db, payload, current_user)

@router.put("/{department_id}", response_model=DepartmentOut)
def update_department(
    department_id: int,
    payload: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin"))
):
    return update_department_service(db, department_id, payload)

@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles("admin")),
):
    return delete_department_service(db, department_id)
