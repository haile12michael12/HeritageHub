from datetime import datetime, timezone
from pathlib import Path
import secrets
import string

from pwdlib import PasswordHash
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, status

from app.core.config import settings
from app.core.exceptions import ApiException
from app.core.security import create_access_token
from app.models.reset_code import ResetCode
from app.models.user import User, UserRole
from app.schemas.user import PasswordUpdate, ResetPasswordRequest, TokenData, UserCreate, UserLogin, UserUpdate
from app.services.email_service import send_reset_password_email, send_welcome_email
from app.services.upload_service import upload_to_s3

password_hasher = PasswordHash.recommended()


async def register_new_user(db: AsyncSession, user_data: UserCreate):
    existing_user = await db.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise ApiException("An account with these details may already exist", status.HTTP_409_CONFLICT)

    user_object = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=password_hasher.hash(user_data.password),
        role=UserRole.CUSTOMER,
    )
    db.add(user_object)
    await db.commit()
    await db.refresh(user_object)
    await send_welcome_email(user_object.email, user_object.name)
    return user_object


async def login_user(db: AsyncSession, login_data: UserLogin) -> TokenData:
    user = await db.scalar(select(User).where(User.email == login_data.email))
    if not user or not user.active or not user.hashed_password:
        raise ApiException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)
    if not password_hasher.verify(login_data.password, user.hashed_password):
        raise ApiException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)
    return TokenData(token=create_access_token({"sub": str(user.id)}), user=user)


async def process_forgot_password(db: AsyncSession, email: str) -> bool:
    user = await db.scalar(select(User).where(User.email == email))
    if not user:
        return True

    await db.execute(delete(ResetCode).where(ResetCode.email == email))
    code = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    db.add(ResetCode(email=email, code=code))
    await db.commit()
    reset_url = f"{settings.RESET_PASSWORD_URL}{code}"
    await send_reset_password_email(email=email, name=user.name, code=code, reset_url=reset_url)
    return True


async def process_reset_password(db: AsyncSession, reset_data: ResetPasswordRequest) -> bool:
    reset_entry = await db.scalar(select(ResetCode).where(ResetCode.code == reset_data.code))
    if not reset_entry:
        raise ApiException("Invalid or expired reset code", status.HTTP_400_BAD_REQUEST)

    current_time = datetime.now(timezone.utc)
    expiry_time = reset_entry.expires_at
    if expiry_time.tzinfo is None:
        expiry_time = expiry_time.replace(tzinfo=timezone.utc)
    if current_time > expiry_time:
        await db.delete(reset_entry)
        await db.commit()
        raise ApiException("Invalid or expired reset code", status.HTTP_400_BAD_REQUEST)

    user = await db.scalar(select(User).where(User.email == reset_entry.email))
    if not user:
        await db.execute(delete(ResetCode).where(ResetCode.email == reset_entry.email))
        await db.commit()
        raise ApiException("Invalid or expired reset code", status.HTTP_400_BAD_REQUEST)

    user.hashed_password = password_hasher.hash(reset_data.password)
    await db.execute(delete(ResetCode).where(ResetCode.email == reset_entry.email))
    await db.commit()
    return True


async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.scalars(select(User).order_by(desc(User.id)))
    return list(result.all())


async def update_user_profile(db: AsyncSession, user: User, update_data: UserUpdate) -> User:
    if update_data.name:
        user.name = update_data.name
    if update_data.address:
        user.address = update_data.address
    await db.commit()
    await db.refresh(user)
    return user


async def change_user_password(db: AsyncSession, user: User, password_data: PasswordUpdate) -> bool:
    if not user.hashed_password or not password_hasher.verify(password_data.old_password, user.hashed_password):
        raise ApiException("Old password is incorrect", status.HTTP_400_BAD_REQUEST)
    user.hashed_password = password_hasher.hash(password_data.new_password)
    await db.commit()
    return True


async def upload_profile_pix(db: AsyncSession, user: User, file: UploadFile) -> str:
    image_path = await upload_to_s3(file=file, upload_dir=Path("uploads/profile"))
    user.profile_picture = image_path
    await db.commit()
    await db.refresh(user)
    return image_path
