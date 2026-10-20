from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(Integer, default=None, index=True)
    action: Mapped[str] = mapped_column(String, index=True)
    resource: Mapped[str] = mapped_column(String)
    resource_id: Mapped[str | None] = mapped_column(String, default=None)
    ip_address: Mapped[str | None] = mapped_column(String, default=None)
    user_agent: Mapped[str | None] = mapped_column(String, default=None)
    details: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
