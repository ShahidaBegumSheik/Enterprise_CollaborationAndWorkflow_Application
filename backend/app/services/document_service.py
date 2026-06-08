import os
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.repositories import document_repository as repo
from app.repositories import task_repository
from app.utils.file_storage import save_upload
from app.core.logger import logger
import asyncio
from app.services.audit_service import create_audit_log
from app.services.subscription_service import get_or_create_subscription
from app.services.notification_service import create_notification
from app.websockets.connection_manager import manager

def get_upload_file_size(file: UploadFile) -> int:
    current_position = file.file.tell()
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()

    file.file.seek(current_position)
    return file_size

def validate_document_storage_limit(db: Session, user, new_file_size: int):
    if not user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not linked to an organization",
        )

    subscription = get_or_create_subscription(
        db,
        user.organization_id,
    )

    used_storage_bytes = repo.get_used_storage_bytes_by_organization(
        db,
        user.organization_id,
    )

    max_storage_bytes = subscription.max_storage_mb * 1024 * 1024

    if used_storage_bytes + new_file_size > max_storage_bytes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Storage limit exceeded. Please upgrade your subscription plan.",
        )
    
    if used_storage_bytes >= int(max_storage_bytes * 0.8):
        create_notification(
            db=db,
            user_id=user.id,
            title="Storage Usage warning",
            message=f"Your organization has used more than 80% of its document storage limit.",
            category="billing",
        )



def upload_document_service(db: Session, file: UploadFile, user, task_id: int | None = None, approval_request_id: int | None = None):
    if not user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user is not linked to an organization")
    
    if task_id == 0:
        task_id = None

    if approval_request_id == 0:
        approval_request_id = None
    
    file_size = get_upload_file_size(file)

    validate_document_storage_limit(
        db=db,
        user=user,
        new_file_size=file_size,
    )

    logger.info(f"Uploading file {file.filename} by user {user.email}")
            
    latest = repo.get_latest_version(db, file.filename, user.organization_id)
    version = latest.version + 1 if latest else 1

    stored_name, file_path = save_upload(file)

    doc = Document(
        original_name=file.filename,
        stored_name=stored_name,
        file_path=file_path,
        file_size=file_size,
        version=version,
        uploaded_by=user.id,
        organization_id=user.organization_id,
        task_id=task_id,
        approval_request_id=approval_request_id,
    )

    logger.info(f"Document uploaded successfully: {stored_name}")

    created = repo.create_document(db, doc)

    create_notification(
        db=db,
        user_id=user.id,
        title="Document Uploaded",
        message=f"Document '{created.original_name}' uploaded successfully",
        category="document",
    )

    create_audit_log(db, user.id, "upload", "document", created.id, f"Document uploaded: {created.original_name}")
    asyncio.create_task(
        manager.broadcast({
            "type": "DOCUMENT_UPLOADED",
            "message": f"Document uploaded: {created.original_name}",
            "document_id": created.id,
            })
    )

    if doc.task_id:
        task = task_repository.get_task_by_id_and_organization(
            db,
            doc.task_id,
            user.organization_id,
        )

        if task and task.assignee_id and task.assignee_id != user.id:
            create_notification(
                db=db,
                user_id=task.assignee_id,
                title="New document added",
                message=f"A document was uploaded for task '{task.title}'",
                category="document",
            )
    
    return created


def list_documents_service(db, user):
    if not user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not linked to an organization")
    
    return repo.list_documents_by_organization(db, user.organization_id)


def get_document_service(db: Session, document_id: int, user):
    doc = repo.get_document_by_id(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.organization_id != user.organization_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to access this document")
    return doc


def delete_document_service(db: Session, document_id: int, user):
    doc = get_document_service(db, document_id, user)
    filename = doc.original_name
    repo.delete_document(db, doc)
    create_audit_log(
        db,
        user.id,
        "delete",
        "document",
        document_id,
        f"Document deleted: {doc.original_name}",
    )

    create_notification(
        db=db,
        user_id=user.id,
        title="Document Deleted",
        message=f"Document  {filename} was deleted",
        category="document",
    )
    
    return {"message": "Document deleted successfully"}
