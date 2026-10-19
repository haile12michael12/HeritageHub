from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ApiException
from app.core.security import decode_access_token
from app.db.database import db_session
from app.models.user import User, UserRole

http_bearer = HTTPBearer(auto_error=True)


async def get_current_user(
    db: AsyncSession = Depends(db_session),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    payload = decode_access_token(token.credentials)
    user_id = payload.get("sub")

    # decode_access_token validates the subject format before it reaches the DB.
    user = await db.get(User, int(user_id))

    if not user or not user.active:
        raise ApiException(
            "Could not validate credentials", status.HTTP_401_UNAUTHORIZED
        )

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise ApiException(
            "You do not have administrative privileges",
            status.HTTP_403_FORBIDDEN,
        )

    return current_user


async def get_current_admin_or_delivery(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role not in (UserRole.ADMIN, UserRole.DELIVERY):
        raise ApiException(
            "You do not have permission to access this resource",
            status.HTTP_403_FORBIDDEN,
        )
    return current_user
