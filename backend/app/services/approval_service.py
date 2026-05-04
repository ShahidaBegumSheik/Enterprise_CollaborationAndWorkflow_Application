from fastapi import HTTPException
from app.models.approval import ApprovalRequest, ApprovalHistory
from app.repositories import approval_repository as repo
from app.repositories.user_repository import list_users

HIGH_VALUE = 10000


def create_request_service(db, payload, user):
    request = ApprovalRequest(
        request_type=payload.request_type,
        title=payload.title,
        description=payload.description,
        amount=payload.amount,
        submitted_by=user.id,
        status="pending_manager",
    )
    return repo.create_request(db, request)


def list_requests_service(db, user):
    if user.role == "employee":
        return repo.list_requests_by_user(db, user.id)
    return repo.list_requests(db)


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
            admins = [u for u in list_users(db) if u.role == "admin"]
            request.status = "pending_admin"
            request.current_approver_id = admins[0].id if admins else None
        else:
            request.status = "approved"
            request.current_approver_id = None

    elif action == "transfer_admin":
        if user.role != "manager":
            raise HTTPException(status_code=403, detail="Only manager can transfer to admin")

        admins = [u for u in list_users(db) if u.role == "admin"]
        request.status = "pending_admin"
        request.current_approver_id = admins[0].id if admins else None

    elif action == "reject":
        request.status = "rejected"
        request.current_approver_id = None

    elif action == "hold":
        request.status = "on_hold"

    else:
        raise HTTPException(status_code=400, detail="Invalid approval action")


    db.commit()
    db.refresh(request)
    return request


def get_approval_history_service(db, request_id):
    return repo.get_history_by_request(db, request_id)
