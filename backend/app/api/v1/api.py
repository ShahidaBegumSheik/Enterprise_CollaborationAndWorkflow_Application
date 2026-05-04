from fastapi import APIRouter
from app.api.v1.endpoints import auth, users,tasks, approvals, documents, dashboard, audit_logs

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tasks.router)
api_router.include_router(approvals.router)
api_router.include_router(documents.router)
api_router.include_router(dashboard.router)
api_router.include_router(audit_logs.router)

