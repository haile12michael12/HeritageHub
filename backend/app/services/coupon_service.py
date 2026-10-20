from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from app.core.exceptions import ApiException
from app.models.coupon import Coupon, DiscountType

async def create_coupon(db: AsyncSession, data: dict):
    code = data["code"].upper().strip()
    existing = await db.scalar(select(Coupon).where(Coupon.code == code))
    if existing:
        raise ApiException("Coupon code already exists", status.HTTP_400_BAD_REQUEST)
    coupon = Coupon(**{**data, "code": code})
    db.add(coupon)
    await db.commit()
    await db.refresh(coupon)
    return coupon

async def list_coupons(db: AsyncSession):
    result = await db.scalars(select(Coupon).order_by(Coupon.created_at.desc()))
    return list(result.all())

async def validate_coupon(db: AsyncSession, code: str, order_amount: Decimal):
    coupon = await db.scalar(select(Coupon).where(Coupon.code == code.upper().strip()))
    if not coupon:
        return {"valid": False, "discount": Decimal("0"), "final_amount": order_amount, "message": "Invalid coupon code"}
    if not coupon.is_active:
        return {"valid": False, "discount": Decimal("0"), "final_amount": order_amount, "message": "Coupon is inactive"}
    if coupon.expires_at and coupon.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return {"valid": False, "discount": Decimal("0"), "final_amount": order_amount, "message": "Coupon has expired"}
    if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
        return {"valid": False, "discount": Decimal("0"), "final_amount": order_amount, "message": "Coupon usage limit reached"}
    if order_amount < coupon.min_order_amount:
        return {"valid": False, "discount": Decimal("0"), "final_amount": order_amount, "message": f"Minimum order amount is {coupon.min_order_amount}"}
    # Calculate discount
    if coupon.discount_type == DiscountType.PERCENTAGE:
        discount = (order_amount * coupon.discount_value / Decimal("100")).quantize(Decimal("0.01"))
        if coupon.max_discount_amount and discount > coupon.max_discount_amount:
            discount = coupon.max_discount_amount
    elif coupon.discount_type == DiscountType.FIXED:
        discount = min(coupon.discount_value, order_amount)
    else:
        discount = Decimal("0")
    final = max(order_amount - discount, Decimal("0"))
    return {"valid": True, "discount": discount, "final_amount": final, "message": f"Coupon applied! You save {discount}"}

async def apply_coupon(db: AsyncSession, code: str):
    coupon = await db.scalar(select(Coupon).where(Coupon.code == code.upper().strip()))
    if coupon:
        coupon.used_count += 1
        await db.commit()
