from fastapi import HTTPException, status

from app.models.department import Department
from app.repositories import department_repository as repo
from app.utils.sanitize import clean_text

def list_departments_service(db):
    return repo.list_departments(db)


def create_department_service(db, payload, user):
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User is not linked to an organization",
        )
    department = Department(
        name=clean_text(payload.name),
        description=clean_text(payload.description),
        organization_id=user.organization_id,
    )
    return repo.create_department(db, department)

def update_department_service(db, department_id: int, payload):
    department = repo.get_department_by_id(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department Not Found")
    
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(department, field, clean_text(value) if isinstance(value, str) else value)
    
    return repo.update_department(db, department)

def delete_department_service(db, department_id: int):
    department = repo.get_department_by_id(db, department_id)

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department Not Found")
    
    repo.delete_department(db, department)

    return {"message": "Department Deleted Successfully"}