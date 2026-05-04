from fastapi import HTTPException, status
from app.models.task import Task
from app.repositories import task_repository as repo
from app.services.audit_service import create_audit_log


def get_task_service(db, task_id, user):
    task = repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    if user.role == "employee" and task.assignee_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

    if user.role == "manager":
        if task.created_by != user.id and task.assignee_id != user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")

    return task_to_out(task)


def list_tasks_service(db, user):
    if user.role == "employee":
        return [task_to_out(task) for task in repo.list_tasks_for_employee(db, user.id)]
    if user.role == "manager":
        return [task_to_out(task) for task in repo.list_tasks_for_manager(db, user.id)]
    return [task_to_out(task) for task in repo.list_all_tasks(db)]


def create_task_service(db, payload, user):
    if user.role not in ["admin", "manager", "employee"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin/Manager role required")

    task = Task(**payload.model_dump(), created_by=user.id)
    task = repo.create_task(db, task)
    task = repo.get_task_by_id(db, task.id)
    create_audit_log(db, user.id, "create", "task", task.id, task.title)
    return task_to_out(task)


def update_task_service(db, task_id, payload, user):
    task = repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    update_data = payload.model_dump(exclude_unset=True)

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

    db.commit()
    db.refresh(task)
    task = repo.get_task_by_id(db, task.id)
    create_audit_log(db, user.id, "update", "task", task.id, task.title)
    return task_to_out(task)


def delete_task_service(db, task_id, user):
    if user.role not in ["admin", "manager"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin/Manager role required")

    task = repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    repo.delete_task(db, task)
    create_audit_log(db, user.id, "delete", "task", task_id, "Task deleted")
    return {"message": "Deleted"}

def task_to_out(task):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date,
        "created_by": task.created_by,
        "assignee_id": task.assignee_id,
        "workspace_id": task.workspace_id,
        "creator_name": task.creator.full_name if task.creator else None,
        "assignee_name": task.assignee.full_name if task.assignee else None,
    }
