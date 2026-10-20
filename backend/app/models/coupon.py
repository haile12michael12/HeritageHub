from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from sqlalchemy import String, DateTime, Numeric, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_SHIPPING = "free_shipping"

class Coupon(Base):
    __tablename__ = "coupons"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    discount_type: Mapped[DiscountType] = mapped_column(SQLEnum(DiscountType), default=DiscountType.PERCENTAGE)
    discount_value: Mapped[Decimal] = mapped_column(Numeric(10,2), default=Decimal("0.00"))
    min_order_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), default=Decimal("0.00"))
    max_discount_amount: Mapped[Decimal | None] = mapped_column(Numeric(10,2), default=None)
    usage_limit: Mapped[int | None] = mapped_column(default=None)
    used_count: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
