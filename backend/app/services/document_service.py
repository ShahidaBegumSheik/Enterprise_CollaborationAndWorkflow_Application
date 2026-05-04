from fastapi import HTTPException
from app.models.document import Document
from app.repositories import document_repository as repo
from app.utils.file_storage import save_upload


def upload_document_service(db, file, user, task_id=None, approval_request_id=None):
    if task_id == 0:
        task_id = None

    if approval_request_id == 0:
        approval_request_id = None
        
    latest = repo.get_latest_version(db, file.filename)
    version = latest.version + 1 if latest else 1

    stored_name, file_path = save_upload(file)

    doc = Document(
        original_name=file.filename,
        stored_name=stored_name,
        file_path=file_path,
        version=version,
        uploaded_by=user.id,
        task_id=task_id,
        approval_request_id=approval_request_id,
    )
    return repo.create_document(db, doc)


def list_documents_service(db):
    return repo.list_documents(db)


def get_document_service(db, document_id):
    doc = repo.get_document_by_id(db, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


def delete_document_service(db, document_id):
    doc = get_document_service(db, document_id)
    repo.delete_document(db, doc)
    return {"message": "Document deleted successfully"}
