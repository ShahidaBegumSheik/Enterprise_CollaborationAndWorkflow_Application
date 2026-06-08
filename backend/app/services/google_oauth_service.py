import httpx
from fastapi import HTTPException, status
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.repositories import user_repository as user_repo
from app.core.security import create_access_token, create_refresh_token


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def get_google_auth_url():
    if not settings.google_client_id or not settings.google_redirect_uri:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured",
        )

    return (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={settings.google_client_id}"
        f"&redirect_uri={settings.google_redirect_uri}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=consent"
    )


async def exchange_code_for_google_user(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google token exchange failed",
            )

        token_data = token_response.json()
        google_access_token = token_data.get("access_token")

        user_response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {google_access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to fetch Google user profile",
            )

        return user_response.json()


async def google_login_service(db: Session, code: str):
    google_user = await exchange_code_for_google_user(code)

    email = google_user.get("email")
    full_name = google_user.get("name") or email

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Google account email not found",
        )

    user = user_repo.get_user_by_email(db, email)

    if not user:
        user = User(
            email=email,
            full_name=full_name,
            password_hash="GOOGLE_OAUTH_USER",
            role="employee",
            is_active=True,
            organization_id=1,
        )
        user = user_repo.create_user(db, user)

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    params = urlencode({
        "access_token": access_token,
        "refresh_token": refresh_token,
    })

    return RedirectResponse(
        url=f"http://localhost:5173/oauth-success?{params}",
        status_code=303,
    )


