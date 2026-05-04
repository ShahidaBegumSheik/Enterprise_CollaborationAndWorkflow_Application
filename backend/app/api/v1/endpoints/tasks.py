from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import *

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_tasks_service(db, user)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return get_task_service(db, task_id, user)


@router.post("", response_model=TaskOut)
def create_task(payload: TaskCreate, db=Depends(get_db), user=Depends(get_current_user)):
    return create_task_service(db, payload, user)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db=Depends(get_db), user=Depends(get_current_user)):
    return update_task_service(db, task_id, payload, user)


@router.delete("/{task_id}")
def delete_task(task_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return delete_task_service(db, task_id, user)
