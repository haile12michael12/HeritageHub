import os
from datetime import datetime, timezone

# Settings are instantiated at import time; use non-secret test-only values.
_TEST_ENV = {
    "DATABASE_URL": "sqlite+aiosqlite:///./test.db",
    "SECRETE_JWT_KEY": "test-only-key-that-must-never-be-used-in-production",
    "MAIL_USER": "test@example.invalid",
    "MAIL_PASS": "test-only",
    "MAIL_HOST": "localhost",
    "MAIL_PORT": "1025",
    "MAIL_FROM": "test@example.invalid",
    "DELIVERY_PERSON_EMAIL": "delivery@example.invalid",
    "BACKEND_URL": "http://localhost:8000",
    "FRONTEND_URL": "http://localhost:5173",
    "RESET_PASSWORD_URL": "http://localhost:5173/reset-password?code=",
    "GOOGLE_CLIENT_ID": "test-client-id",
    "GOOGLE_CLIENT_SECRET": "test-client-secret",
    "GOOGLE_AUTH_BASE_URL": "https://accounts.google.com/o/oauth2/v2/auth",
    "GOOGLE_REDIRECT_URL": "http://localhost:8000/api/auth/google/callback",
    "AWS_ACCESS_KEY": "test",
    "AWS_SECRET_KEY": "test",
    "AWS_BUCKET_NAME": "test",
    "AWS_BUCKET_REGION": "us-east-1",
    "STRIPE_SECRET_KEY": "test",
    "PAYMENT_CONFIRMATION_URL": "http://localhost:5173/payment/success",
    "PAYMENT_CANCEL_URL": "http://localhost:5173/payment/cancel",
}
for key, value in _TEST_ENV.items():
    os.environ.setdefault(key, value)

import jwt
import pytest
from pydantic import ValidationError

from app.core.exceptions import ApiException
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRETE_JWT_KEY,
    decode_access_token,
    create_access_token,
)
from app.schemas.user import UserCreate


def test_public_registration_ignores_client_supplied_admin_role():
    payload = UserCreate.model_validate(
        {
            "email": "customer@example.com",
            "name": "Example Customer",
            "password": "correct-horse-battery",
            "role": "ADMIN",
        }
    )
    assert not hasattr(payload, "role")


def test_registration_requires_long_password():
    with pytest.raises(ValidationError):
        UserCreate.model_validate(
            {
                "email": "customer@example.com",
                "name": "Example Customer",
                "password": "short",
                "role": "CUSTOMER",
            }
        )


def test_access_token_is_short_lived_and_has_subject():
    token = create_access_token({"sub": "123"})
    payload = decode_access_token(token)
    now = int(datetime.now(timezone.utc).timestamp())

    assert payload["sub"] == "123"
    assert payload["exp"] > now
    assert payload["exp"] - now <= ACCESS_TOKEN_EXPIRE_MINUTES * 60 + 1
    assert "role" not in payload


def test_access_token_rejects_non_numeric_subject():
    token = jwt.encode(
        {
            "sub": "not-a-user-id",
            "exp": int(datetime.now(timezone.utc).timestamp()) + 60,
        },
        SECRETE_JWT_KEY,
        algorithm="HS256",
    )
    with pytest.raises(ApiException):
        decode_access_token(token)
