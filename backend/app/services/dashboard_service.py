import json

from fastapi import HTTPException, status

from app.core.redis_client import redis_client
from app.core.config import settings
from app.repositories import dashboard_repository as repo
from app.services.ai_service import generate_dashboard_ai_summary


def _safe_cache_get(key: str):
    try:
        cached = redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception:
        return None


def _safe_cache_set(key: str, value: dict):
    try:
        redis_client.setex(
            key,
            settings.cache_ttl_seconds,
            json.dumps(value),
        )
    except Exception:
        pass


def clear_dashboard_cache():
    try:
        for key in redis_client.scan_iter("dashboard_summary:*"):
            redis_client.delete(key)
    except Exception:
        pass


def get_dashboard_summary_service(db, user):
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to an organization",
        )

    role = str(user.role or "").lower()
    cache_key = f"dashboard_summary:{role}:{user.organization_id}:{user.id}"

    cached = _safe_cache_get(cache_key)
    if cached:
        return cached

    if role == "employee":
        summary = employee_dashboard(db, user)
    elif role == "manager":
        summary = manager_dashboard(db, user)
    else:
        summary = admin_dashboard(db, user)

    _safe_cache_set(cache_key, summary)
    return summary


def employee_dashboard(db, user):
    task_summary = repo.get_employee_task_summary(
        db,
        user.organization_id,
        user.id,
    )

    summary = {
        "role": "employee",
        **task_summary,
        "my_requests": repo.count_employee_requests(
            db,
            user.organization_id,
            user.id,
        ),
        "pending_requests": repo.count_employee_pending_requests(
            db,
            user.organization_id,
            user.id,
        ),
        "approved_requests": repo.count_employee_approved_requests(
            db,
            user.organization_id,
            user.id,
        ),
    }

    summary["ai_summary"] = generate_dashboard_ai_summary("employee", summary)
    return summary


def manager_dashboard(db, user):
    task_summary = repo.get_manager_task_summary(
        db,
        user.organization_id,
        user.id,
    )

    summary = {
        "role": "manager",
        "team_tasks": task_summary["total_tasks"],
        **task_summary,
        "pending_approvals": repo.count_manager_pending_approvals(
            db,
            user.organization_id,
        ),
        "on_hold_approvals": repo.count_on_hold_approvals(
            db,
            user.organization_id,
        ),
        "transferred_to_admin": repo.count_transferred_to_admin(
            db,
            user.organization_id,
        ),
    }

    summary["ai_summary"] = generate_dashboard_ai_summary("manager", summary)
    return summary


def admin_dashboard(db, user):
    task_summary = repo.get_admin_task_summary(
        db,
        user.organization_id,
    )

    summary = {
        "role": "admin",
        **task_summary,
        "total_users": repo.count_users_by_organization(
            db,
            user.organization_id,
        ),
        "total_documents": repo.count_documents_by_organization(
            db,
            user.organization_id,
        ),
        "total_approvals": repo.count_approvals_by_organization(
            db,
            user.organization_id,
        ),
        "pending_admin_approvals": repo.count_transferred_to_admin(
            db,
            user.organization_id,
        ),
    }

    summary["ai_summary"] = generate_dashboard_ai_summary("admin", summary)
    return summary

