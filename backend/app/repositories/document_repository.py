from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.document import Document
from app.utils.db_exceptions import handle_db_commit

from fastapi_pagination.ext.sqlalchemy import paginate


def get_latest_version(db, filename):
    stmt = (
        select(Document)
        .where(Document.original_name == filename)
        .order_by(Document.version.desc())
    )
    return db.execute(stmt).scalars().first()


def create_document(db: Session, doc: Document):
    db.add(doc)
    handle_db_commit(db)
    db.refresh(doc)
    return doc


def list_documents(db: Session):
    stmt = select(Document).order_by(Document.id.desc())
    return paginate(db, stmt)


def list_documents_by_organization(db: Session, organization_id: int):
    stmt = (
        select(Document)
        .where(Document.organization_id == organization_id)
        .order_by(Document.id.desc())
    )
    return paginate(db, stmt)


def get_document_by_id(db: Session, document_id: int):
    return db.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()


def delete_document(db: Session, doc: Document):
    db.delete(doc)
    handle_db_commit(db)
    

def get_used_storage_bytes_by_organization(
    db: Session,
    organization_id: int,
):
    return (
        db.execute(
            select(func.coalesce(func.sum(Document.file_size), 0))
            .where(Document.organization_id == organization_id)
        ).scalar() or 0
    )

