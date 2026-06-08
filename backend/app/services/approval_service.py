from fastapi import HTTPException, status
from app.models.approval import ApprovalRequest, ApprovalHistory
from app.repositories import approval_repository as repo
from app.repositories.user_repository import list_admin_users_by_organization, list_manager_users_by_organization
from app.utils.sanitize import clean_text
import asyncio
from app.services.audit_service import create_audit_log
from app.services.notification_service import create_notification
from app.websockets.connection_manager import manager

HIGH_VALUE = 10000


async def create_request_service(db, payload, user):
    if not user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not linked to an organization")
    role = str(user.role).lower()

    if role == "manager":
        initial_status = "pending_admin"
    else:
        initial_status = "pending_manager"

    request = ApprovalRequest(
        request_type=clean_text(payload.request_type),
        title=clean_text(payload.title),
        description=clean_text(payload.description),
        amount=payload.amount,
        submitted_by=user.id,
        organization_id=user.organization_id,
        status=initial_status,
    )

    created = repo.create_request(db, request)

    if initial_status == "pending_manager":
        managers = list_manager_users_by_organization(
            db,
            user.organization_id,
        )

        for manager_user in managers:
            create_notification(
                db=db,
                user_id=manager_user.id,
                title="Approval request pending",
                message=f"Approval request '{created.title}' needs manager decision.",
                category="approval",
            )

    elif initial_status == "pending_admin":
        admins = list_admin_users_by_organization(
            db,
            user.organization_id,
        )

        for admin_user in admins:
            create_notification(
                db=db,
                user_id=admin_user.id,
                title="Approval pending admin",
                message=f"Approval request '{created.title}' needs admin decision.",
                category="approval",
            )

    create_audit_log(
        db, user.id, "create", "approval", created.id, f"Approval request created: {created.title}"
    )

    await manager.broadcast({
            "type": "APPROVAL CREATED",
            "message": f"New approval request: {created.title}",
            "approval_id": created.id,
            "status": created.status,
    })
    return created


def list_requests_service(db, user):
    role = str(user.role).lower()

    if not user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not linked to an organozation")
    
    if role == "employee":
        return repo.list_requests_by_user(db, user.id, user.organization_id)
    if role == "manager":
        return repo.list_requests_by_manager(db, user.organization_id)

    return repo.list_requests_by_organization(db, user.organization_id)


def approval_action_service(db, request_id, payload, user):
    request = repo.get_request_by_id(db, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if request.submitted_by == user.id:
        raise HTTPException(status_code=403, detail="Requester cannot approve their own request")

    if request.status == "pending_manager" and user.role != "manager":
        raise HTTPException(status_code=403, detail="Only manager can approve this request")

    if request.status == "pending_admin" and user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can approve this request")

    history = ApprovalHistory(
        approval_request_id=request_id,
        action=payload.action,
        comment=payload.comment,
        acted_by=user.id,
    )
    repo.add_history(db, history)

    action = payload.action.lower()

    if action == "approve":
        if user.role == "manager" and request.amount and request.amount > HIGH_VALUE:
            admins = list_admin_users_by_organization(db, request.organization_id)
            request.status = "pending_admin"
            request.current_approver_id = admins[0].id if admins else None
            for admin_user in admins:
                create_notification(
                    db=db,
                    user_id=admin_user.id,
                    title="High-value approval pending",
                    message=f"High-value approval request '{request.title}' needs admin decision.",
                    category="approval",
                )
        else:
            request.status = "approved"
            request.current_approver_id = None
            create_notification(
                db=db,
                user_id=request.submitted_by,
                title="Request Approved",
                message=f"{request.title} has been approved",
                category="approval",
            )
    elif action == "transfer_admin":
        if user.role != "manager":
            raise HTTPException(status_code=403, detail="Only manager can transfer to admin")

        admins = list_admin_users_by_organization(db, user.organization_id)
        request.status = "pending_admin"
        request.current_approver_id = admins[0].id if admins else None
        for admin_user in admins:
            create_notification(
                db=db,
                user_id=admin_user.id,
                title="High-value approval pending",
                message=f"High-value approval request '{request.title}' needs admin decision.",
                category="approval",
            )

    elif action == "reject":
        request.status = "rejected"
        request.current_approver_id = None
        create_notification(
            db=db,
            user_id=request.submitted_by,
            title="Request Rejected",
            message=f"{request.title} has been rejected",
            category="approval",
        )

    elif action == "hold":
        request.status = "on_hold"
        create_notification(
            db=db,
            user_id=request.submitted_by,
            title="Request on hold",
            message=f"{request.title} has been put on hold",
            category="approval",
        )

    else:
        raise HTTPException(status_code=400, detail="Invalid approval action")


    request = repo.update_request(db, request)

    create_audit_log(
        db, user.id, action, "approval", request.id, f"Approval {action} created: {request.title}"
    )

    asyncio.create_task(
        manager.broadcast({
            "type": "APPROVAL UPDATED",
            "message": f"Approval {action}: {request.title}",
            "approval_id": request.id,
            "status": request.status,
        })
    )

    return request


def get_approval_history_service(db, request_id):
    return repo.get_history_by_request(db, request_id)
