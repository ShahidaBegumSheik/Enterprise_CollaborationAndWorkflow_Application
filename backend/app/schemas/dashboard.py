from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_tasks: int
    done_tasks: int
    pending_tasks: int
    todo_tasks: int
    in_progress_tasks: int
    review_tasks: int