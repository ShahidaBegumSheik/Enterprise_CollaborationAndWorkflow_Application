from sqlalchemy import select
from app.models.document import Document


def get_latest_version(db, filename):
    stmt = (
        select(Document)
        .where(Document.original_name == filename)
        .order_by(Document.version.desc())
    )
    return db.execute(stmt).scalars().first()


def create_document(db, doc):
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def list_documents(db):
    return db.execute(select(Document)).scalars().all()


def get_document_by_id(db, document_id: int):
    return db.execute(
        select(Document).where(Document.id == document_id)
    ).scalar_one_or_none()


def delete_document(db, doc):
    db.delete(doc)
    db.commit()
