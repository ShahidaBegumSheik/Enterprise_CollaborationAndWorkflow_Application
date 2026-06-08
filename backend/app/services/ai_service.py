from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.task import Task
from app.repositories import ai_repository as repo


def calculate_delay_risk(task: Task):
    score = 0
    reasons = []

    if task.priority == "high":
        score += 30
        reasons.append("High Priority Task")

    if task.status in ["todo", "in_progress", "review"]:
        score += 20
        reasons.append("Task is still pending")

    if task.due_date:
        now = datetime.now(timezone.utc)
        due_date = task.due_date

        if due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=timezone.utc)
        
        if due_date < now:
            score += 40
            reasons.append("Task is overdue")
        else:
            days_left = (due_date - now).days

            if days_left <= 1:
                score += 25
                reasons.append("Due date is very near")
            elif days_left <= 3:
                score += 15
                reasons.append("Due within 3 days")
    if score >= 70:
        risk = "high"
    elif score >= 40:
        risk = "medium"
    else:
        risk = "low"
    
    return {
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons,
    }
    

def get_ai_task_insights_service(db: Session, user):
    tasks = repo.list_pending_tasks_by_organization(db, user.organization_id)

    insights = []

    for task in tasks:
        risk = calculate_delay_risk(task)

        if task.priority == "high" or risk["risk_level"] in ["high", "medium"]:
            insights.append({
                "task_id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "due_date": str(task.due_date) if task.due_date else None,
                "risk_score": risk["risk_score"],
                "risk_level": risk["risk_level"],
                "reasons": risk["reasons"],
            })

    return {
        "total_flagged_tasks": len(insights),
        "insights": insights,
    }

def get_user_workload(db: Session, user_id: int, organization_id: int):
    pending = repo.count_pending_tasks_for_user(db, user_id, organization_id)
    completed = repo.count_completed_tasks_for_user(db, user_id, organization_id)
    overdue = repo.count_overdue_tasks_for_user(db, user_id, organization_id)
    return pending, completed, overdue


def recommend_assignee_service(db: Session, user):
    employees = repo.list_active_employees_by_organization(db, user.organization_id)

    recommendations = []

    for employee in employees:
        pending, completed, overdue = get_user_workload(db, employee.id, user.organization_id)

        score = 100
        score -= pending * 10
        score -= overdue * 20
        score += completed * 3

        recommendations.append({
            "user_id": employee.id,
            "name": employee.full_name,
            "email": employee.email,
            "pending_tasks": pending,
            "completed_tasks": completed,
            "overdue_tasks": overdue,
            "assignment_score": score,
        })

    recommendations.sort(
        key=lambda item: item["assignment_score"],
        reverse=True,
    )

    return {
        "recommended_user": recommendations[0] if recommendations else None,
        "all_candidates": recommendations,
    }


def generate_dashboard_ai_summary(role: str, summary: dict):
    role = str(role or "").lower()

    total_tasks = summary.get("total_tasks", 0)
    done_tasks = summary.get("done_tasks", 0)
    pending_tasks = summary.get("pending_tasks", 0)
    review_tasks = summary.get("review_tasks", 0)

    pending_requests = summary.get("pending_requests", 0)
    pending_approvals = summary.get("pending_approvals", 0)
    pending_admin_approvals = summary.get("pending_admin_approvals", 0)
    on_hold_approvals = summary.get("on_hold_approvals", 0)

    total_users = summary.get("total_users", 0)
    total_documents = summary.get("total_documents", 0)

    completion_rate = 0
    if total_tasks:
        completion_rate = round((done_tasks / total_tasks) * 100)

    if role == "employee":
        if pending_tasks > 0:
            return (
                f"You have {pending_tasks} pending task(s). "
                f"Your completion rate is {completion_rate}%. "
                f"Focus on completing assigned tasks before taking new work."
            )

        if pending_requests > 0:
            return (
                f"You have {pending_requests} approval request(s) still pending. "
                f"Track their status and follow up if needed."
            )

        return (
            "Your assigned work is in good condition. "
            "No urgent task or approval action is pending."
        )

    if role == "manager":
        if pending_approvals > 0:
            return (
                f"There are {pending_approvals} approval request(s) waiting for manager decision. "
                f"Review them to avoid workflow delay."
            )

        if review_tasks > 0:
            return (
                f"{review_tasks} task(s) are in review stage. "
                f"Validate deliverables and move completed work to Done."
            )

        if on_hold_approvals > 0:
            return (
                f"{on_hold_approvals} request(s) are on hold. "
                f"Recheck them and decide whether to approve, reject, or transfer."
            )

        return (
            f"Team workflow is stable with {total_tasks} task(s). "
            f"Completion rate is {completion_rate}%."
        )

    if role == "admin":
        if pending_admin_approvals > 0:
            return (
                f"{pending_admin_approvals} request(s) require admin-level decision. "
                f"Prioritize them for governance and compliance."
            )

        return (
            f"System is operating with {total_users} user(s), "
            f"{total_tasks} task(s), and {total_documents} document(s). "
            f"Monitor organization activity and subscription usage."
        )

    return "No AI summary available for this role."


    