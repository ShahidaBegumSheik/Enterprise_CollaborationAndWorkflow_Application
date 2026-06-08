from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import *
from fastapi_pagination import Page

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=Page[TaskOut])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_tasks_service(db, user)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_task_service(db, task_id, user)


@router.post("", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_task_service(db, payload, user)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_task_service(db, task_id, payload, user)

@router.put("/{task_id}/status")
def update_status(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_task_status(db=db, task_id=task_id, status=payload.status, user=user)


@router.delete("/{task_id}")
def delete_task(task_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return delete_task_service(db, task_id, user)
