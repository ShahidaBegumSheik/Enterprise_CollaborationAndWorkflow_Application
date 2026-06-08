from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt

from app.core.config import settings
from app.repositories.user_repository import get_user_by_email
from app.core.database import SessionLocal
from app.websockets.connection_manager import manager

router = APIRouter(tags=["WebSocket"])


def get_user_from_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )

        email = payload.get("sub")

        if not email:
            return None

        db = SessionLocal()
        try:
            return get_user_by_email(db, email)
        finally:
            db.close()

    except JWTError:
        return None


@router.websocket("/ws/notifications")
async def websocket_notifications(
    websocket: WebSocket,
    token: str = Query(...),
):
    user = get_user_from_token(token)

    if not user:
        await websocket.close(code=1008)
        return

    await manager.connect(user.id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(user.id, websocket)

