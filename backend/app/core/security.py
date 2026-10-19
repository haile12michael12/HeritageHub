from datetime import datetime, timedelta, timezone

import jwt
from fastapi import status

from app.core.config import settings
from app.core.exceptions import ApiException

ALGORITHM = "HS256"
SECRETE_JWT_KEY = settings.SECRETE_JWT_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 15

if not SECRETE_JWT_KEY:
    raise RuntimeError("JWT signing key is not configured")


def create_access_token(data: dict) -> str:
    """Create a short-lived signed access token.

    JWT payloads are signed, not encrypted; do not put secrets in claims.
    """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update(
        {
            "iat": now,
            "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
    )
    return jwt.encode(to_encode, SECRETE_JWT_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRETE_JWT_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
        if not isinstance(payload.get("sub"), str) or not payload["sub"].isdigit():
            raise ApiException(
                "Could not validate credentials", status.HTTP_401_UNAUTHORIZED
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise ApiException("Token has expired", status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        raise ApiException("Invalid token", status.HTTP_401_UNAUTHORIZED)
