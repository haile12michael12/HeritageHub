from datetime import datetime
from decimal import Decimal
from app.models.coupon import DiscountType
from app.schemas.schema_base import SchemaBaseModel

class CouponCreate(SchemaBaseModel):
    code: str
    description: str | None = None
    discount_type: DiscountType = DiscountType.PERCENTAGE
    discount_value: Decimal
    min_order_amount: Decimal = Decimal("0.00")
    max_discount_amount: Decimal | None = None
    usage_limit: int | None = None
    expires_at: datetime | None = None

class CouponRead(CouponCreate):
    id: int
    used_count: int
    is_active: bool
    created_at: datetime

class CouponValidateRequest(SchemaBaseModel):
    code: str
    order_amount: Decimal

class CouponValidateResponse(SchemaBaseModel):
    valid: bool
    discount: Decimal
    final_amount: Decimal
    message: str
