from pydantic import EmailStr, Field

from app.models.user import UserRole
from app.schemas.schema_base import SchemaBaseModel


class UserCreate(SchemaBaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name: str


class UserRead(SchemaBaseModel):
    id: int
    email: str
    name: str
    role: UserRole
    active: bool
    profile_picture: str | None = None
    address: str | None = None


class UserLogin(SchemaBaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenData(SchemaBaseModel):
    token: str
    type: str = "bearer"
    user: UserRead


class UserUpdate(SchemaBaseModel):
    name: str | None = None
    address: str | None = None


class PasswordUpdate(SchemaBaseModel):
    old_password: str
    new_password: str = Field(min_length=12, max_length=128)


class ForgotPasswordRequest(SchemaBaseModel):
    email: EmailStr


class ResetPasswordRequest(SchemaBaseModel):
    code: str = Field(min_length=6, max_length=128)
    password: str = Field(min_length=12, max_length=128)
