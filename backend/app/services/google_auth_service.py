import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import User, UserRole
from app.services.email_service import send_welcome_email


async def process_google_callback_workflow(db: AsyncSession, code: str) -> User:
    token_data = await exchange_code_for_token(code)
    access_token = token_data.get("access_token")
    if not access_token:
        raise ValueError("Google authorization failed")

    user_info = await get_user_info(access_token)
    if not user_info.get("email") or not user_info.get("verified_email"):
        raise ValueError("Google account must have a verified email address")

    user = await get_or_create_user_from_google(db, user_info)
    await send_welcome_email(user.email, user.name)
    return user


async def get_or_create_user_from_google(db: AsyncSession, user_data: dict) -> User:
    email = user_data.get("email")
    if not email or not user_data.get("verified_email"):
        raise ValueError("A verified Google email is required")

    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        user = User(
            email=email,
            name=user_data.get("name") or email.split("@")[0],
            hashed_password=None,
            role=UserRole.CUSTOMER,
            profile_picture=user_data.get("picture"),
            active=True,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    elif not user.active:
        raise ValueError("This account is disabled")

    return user


async def get_user_info(access_token: str) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()


async def exchange_code_for_token(code: str) -> dict:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URL,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()


async def generate_user_token(user: User) -> str:
    return create_access_token(data={"sub": str(user.id)})
