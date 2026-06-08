from fastapi import APIRouter
from app.api.v1.endpoints import auth, users,tasks, approvals, documents, dashboard, audit_logs, ws, ai, departments, workspaces, notifications, billing 

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(departments.router)
api_router.include_router(workspaces.router)
api_router.include_router(tasks.router)
api_router.include_router(approvals.router)
api_router.include_router(documents.router)
api_router.include_router(dashboard.router)
api_router.include_router(audit_logs.router)
api_router.include_router(ws.router)
api_router.include_router(ai.router)
api_router.include_router(notifications.router)
api_router.include_router(billing.router)

