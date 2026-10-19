from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import db_session
from app.schemas.response import ApiResponse
from app.schemas.user import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    TokenData,
    UserCreate,
    UserLogin,
    UserRead,
)
from app.services.google_auth_service import (
    generate_user_token,
    process_google_callback_workflow,
)
from app.services.user_service import (
    login_user,
    process_forgot_password,
    process_reset_password,
    register_new_user,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, db: AsyncSession = Depends(db_session)
) -> ApiResponse[UserRead]:
    user = await register_new_user(db=db, user_data=user_data)
    return ApiResponse[UserRead](
        status=status.HTTP_201_CREATED,
        message="User registered successfully",
        data=user,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    login_data: UserLogin, db: AsyncSession = Depends(db_session)
) -> ApiResponse[TokenData]:
    token_info = await login_user(db=db, login_data=login_data)
    return ApiResponse[TokenData](
        status=status.HTTP_200_OK,
        message="Login successful",
        data=token_info,
    )


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request: ForgotPasswordRequest, db: AsyncSession = Depends(db_session)
) -> ApiResponse[None]:
    await process_forgot_password(db, request.email)
    return ApiResponse[None](
        status=status.HTTP_200_OK,
        message="If an account exists for that email, reset instructions will be sent.",
    )


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request: ResetPasswordRequest, db: AsyncSession = Depends(db_session)
) -> ApiResponse[None]:
    await process_reset_password(db, request)
    return ApiResponse[None](
        status=status.HTTP_200_OK, message="Password reset successfully"
    )


@router.get("/google")
async def google_reg_login():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URL,
        "response_type": "code",
        "scope": "email profile",
        "access_type": "offline",
    }
    auth_url = f"{settings.GOOGLE_AUTH_BASE_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/google/callback")
async def google_callback(
    request: Request, code: str | None = None, db: AsyncSession = Depends(db_session)
):
    # Do not echo arbitrary provider error text into a redirect URL.
    if request.query_params.get("error") or not code:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth-error?error=oauth_failed"
        )

    try:
        user = await process_google_callback_workflow(db, code)
        auth_token = await generate_user_token(user)

        # Compatibility note: the frontend must be migrated to a one-time-code
        # exchange or a secure cookie before removing the token query parameter.
        # Never log this redirect URL: it currently contains a bearer credential.
        redirect_url = (
            f"{settings.FRONTEND_URL}/auth-success?"
            f"{urlencode({'token': auth_token, 'role': user.role.value})}"
        )
        return RedirectResponse(url=redirect_url)
    except Exception:
        # Avoid returning exception details, provider payloads, or tokens to clients.
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth-error?error=oauth_failed"
        )
