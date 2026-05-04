from sqlalchemy import select
from app.models.task import Task


def get_dashboard_summary_service(db):
    tasks = db.execute(select(Task)).scalars().all()

    return {
        "total_tasks": len(tasks),
        "done_tasks": len([t for t in tasks if t.status == "done"]),
        "pending_tasks": len([t for t in tasks if t.status != "done"]),
        "todo_tasks": len([t for t in tasks if t.status == "todo"]),
        "in_progress_tasks": len([t for t in tasks if t.status == "in_progress"]),
        "review_tasks": len([t for t in tasks if t.status == "review"]),
    }
