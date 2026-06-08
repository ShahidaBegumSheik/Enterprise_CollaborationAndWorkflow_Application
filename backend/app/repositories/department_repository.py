from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

from app.models.department import Department
from app.utils.db_exceptions import handle_db_commit

def list_departments(db: Session):
    stmt = select(Department).order_by(Department.id.desc())
    return paginate(db, stmt)

def get_department_by_id(db: Session, department_id: int):
    stmt = select(Department).where(Department.id == department_id)
    return db.execute(stmt).scalar_one_or_none()

def create_department(db: Session, department: Department):
    db.add(department)
    handle_db_commit(db)
    db.refresh(department)
    return department

def update_department(db: Session, department: Department):
    handle_db_commit(db)
    db.refresh(department)
    return department

def delete_department(db: Session, department: Department):
    db.delete(department)
    handle_db_commit(db)
