from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import db_session
from app.api.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.coupon import CouponCreate, CouponRead, CouponValidateRequest
from app.services.coupon_service import create_coupon, list_coupons, validate_coupon

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_coupons(db: AsyncSession = Depends(db_session), user: User = Depends(get_current_user)):
    coupons = await list_coupons(db)
    return ApiResponse(status=200, message="Coupons retrieved", data=coupons)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_coupon_endpoint(data: CouponCreate, db: AsyncSession = Depends(db_session), admin: User = Depends(get_current_admin)):
    coupon = await create_coupon(db, data.model_dump())
    return ApiResponse(status=201, message="Coupon created", data=coupon)

@router.post("/validate", status_code=status.HTTP_200_OK)
async def validate_coupon_endpoint(req: CouponValidateRequest, db: AsyncSession = Depends(db_session), user: User = Depends(get_current_user)):
    result = await validate_coupon(db, req.code, req.order_amount)
    return ApiResponse(status=200, message=result["message"], data=result)
