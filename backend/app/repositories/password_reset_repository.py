from sqlalchemy import select
from app.models.password_reset import PasswordResetToken
from app.utils.db_exceptions import handle_db_commit

def create_reset_token(db, reset_token):
    db.add(reset_token)
    handle_db_commit(db)
    db.refresh(reset_token)
    return reset_token

def get_reset_token(db, token: str):
    stmt = select(PasswordResetToken).where(
        PasswordResetToken.token == token
    )
    return db.execute(stmt).scalar_one_or_none()

def update_reset_token(db, reset_token):
    handle_db_commit(db)
    db.refresh(reset_token)
    return reset_token