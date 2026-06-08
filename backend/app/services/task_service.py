from fastapi import HTTPException, status
from fastapi_pagination import Page, create_page
from sqlalchemy.orm import Session
from app.models.task import Task
from app.repositories import task_repository as repo
from app.repositories import user_repository
from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification
from app.schemas.task import TaskOut
from app.utils.sanitize import clean_text
from app.utils.db_exceptions import handle_db_commit
import asyncio
from app.websockets.connection_manager import manager
from app.core.logger import logger


def get_task_service(db, task_id, user):
    task = repo.get_task_by_id_and_organization(db, task_id, user.organization_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    if user.role == "employee" and task.assignee_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

    if user.role == "manager":
        if task.created_by != user.id and task.assignee_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

    return task_to_out(task)


def list_tasks_service(db, user):
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to an organization",
        )
    if user.role == "employee":
        return repo.list_tasks_for_employee(
            db=db, 
            user_id=user.id,
            organization_id=user.organization_id,
        )
    elif user.role == "manager":
        return repo.list_tasks_for_manager(
            db=db, 
            user_id=user.id,
            organization_id=user.organization_id,
        )
    else:
        page = repo.list_tasks_by_organization(
            db=db,
            organization_id=user.organization_id,
        )

    converted_item = [task if isinstance(task, TaskOut) else task_to_out(task) for task in page.items]
    page.items = converted_item
    
    return page

def safe_broadcast(message: dict):
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(manager.broadcast(message))
        except RuntimeError:
            pass
    

def create_task_service(db, payload, user):
    logger.info(f"Task creation started by user {user.email}")
    if user.role not in ["admin", "manager"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin/Manager role required")
    
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to the organozation",
        )
    
    if payload.assignee_id:
        assignee = user_repository.get_valid_assignee_by_id(
            db=db,
            assignee_id=payload.assignee_id,
            organization_id=user.organization_id,
        )

        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assignee for this organization",
            )

        if assignee.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tasks cannot be assigned to yourself",
            )
  
    task = Task(**payload.model_dump(), created_by=user.id, organization_id=user.organization_id)
    task = repo.create_task(db, task)
    task = repo.get_task_by_id_and_organization(db, task.id, user.organization_id)
    create_audit_log(db, user.id, "create", "task", task.id, task.title)
    if task.assignee_id and task.assignee_id != user.id:
        create_notification(
            db=db,
            user_id=task.assignee_id,
            title="New task assigned",
            message=f"You have been assigned task: {task.title}",
            category="task",
        )
    safe_broadcast({
        "type": "TASK_CREATED",
        "message": f"New task created: {task.title}",
        "task_id": task.id,
    })

    logger.info(f"Task created successfully. Task ID={task.id}")
    return task_to_out(task)


def update_task_service(db, task_id, payload, user):
    task = repo.get_task_by_id_and_organization(db, task_id, user.organization_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "assignee_id" in update_data and update_data["assignee_id"]:
        assignee = user_repository.get_valid_assignee_by_id(
            db=db,
            assignee_id=update_data["assignee_id"],
            organization_id=user.organization_id,
        )

        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assignee for this organization",
            )

        if assignee.id == user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tasks cannot be assigned to yourself",
            )

    if user.role == "employee":
        if task.assignee_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
        if any(k != "status" for k in update_data):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Only status update allowed")

    if user.role == "manager":
        if task.created_by != user.id and task.assignee_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

    for k, v in update_data.items():
        setattr(task, k, v)

    repo.update_task(db, task)
    task = repo.get_task_by_id_and_organization(db, task.id, user.organization_id)
    create_audit_log(db, user.id, "update", "task", task.id, task.title)
    
    if task.assignee_id and task.assignee_id != user.id:
        create_notification(
            db=db,
            user_id=task.assignee_id,
            title="Task updated",
            message=f"Task updated: {task.title}",
            category="task",
        )

    safe_broadcast({
        "type": "TASK_UPDATED",
        "message": f"New task updated: {task.title}",
        "task_id": task.id,
        "status": task.status,
    })
    return task_to_out(task)

def update_task_status(db: Session, task_id: int, status: str, user):
    allowed_statuses = ["todo", "in_progress", "review", "done"]

    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid task status")

    task = repo.get_task_by_id_and_organization(db, task_id, user.organization_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if user.role == "employee" and task.assignee_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if user.role == "manager":
        if task.created_by != user.id and task.assignee_id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

    task.status = status
    task = repo.update_task(db, task)

    create_audit_log(db, user.id, "update_status", "task", task.id, f"Status changed to {status}")
    if task.assignee_id:
        create_notification(
            db=db,
            user_id=task.assignee_id,
            title="Task status updated",
            message=f"Task '{task.title}' moved to {status}",
            category="task",
        )

    safe_broadcast({
        "type": "TASK_STATUS_UPDATED",
        "message": f"Task moved to {status}",
        "task_id": task.id,
        "status": task.status,
    })

    return task_to_out(task)


def delete_task_service(db, task_id, user):
    if user.role not in ["admin", "manager"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin/Manager role required")

    task = repo.get_task_by_id_and_organization(db, task_id, user.organization_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")
    
    assignee_id = task.assignee_id
    task_title = task.title

    repo.delete_task(db, task)
    create_audit_log(db, user.id, "delete", "task", task_id, "Task deleted")

    if assignee_id and assignee_id != user.id:
        create_notification(
            db=db,
            user_id=assignee_id,
            title="Task deleted",
            message=f"Task deleted: {task_title}",
            category="task",
        )

    return {"message": "Deleted"}

def task_to_out(task):
    return {
        "id": task.id,
        "title": clean_text(task.title),
        "description": clean_text(task.description),
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "created_by": task.created_by,
        "assignee_id": task.assignee_id,
        "organization_id": task.organization_id,
        "created_at": task.created_at,
        "updated_at": task.updated_at,
    }
