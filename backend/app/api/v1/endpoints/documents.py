from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.document_service import *

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
def upload(
    file: UploadFile = File(...),
    task_id: int | None = Form(None),
    approval_request_id: int | None = Form(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return upload_document_service(db, file, user, task_id, approval_request_id)


@router.get("")
def list_docs(db=Depends(get_db)):
    return list_documents_service(db)


@router.get("/{document_id}")
def get_document(document_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return get_document_service(db, document_id)


@router.get("/{document_id}/download")
def download_document(document_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    doc = get_document_service(db, document_id)
    return FileResponse(path=doc.file_path, filename=doc.original_name)


@router.delete("/{document_id}")
def delete_document(document_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    return delete_document_service(db, document_id)
