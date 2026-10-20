from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import db_session
from app.api.dependencies import get_current_admin
from app.models.user import User, UserRole
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.schemas.response import ApiResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", status_code=status.HTTP_200_OK)
async def analytics_overview(db: AsyncSession = Depends(db_session), admin: User = Depends(get_current_admin)):
    total_orders = (await db.scalar(select(func.count()).select_from(Order))) or 0
    total_revenue = (await db.scalar(select(func.coalesce(func.sum(Order.total_price), 0)).select_from(Order).where(Order.status != OrderStatus.CANCELLED))) or 0
    total_products = (await db.scalar(select(func.count()).select_from(Product))) or 0
    total_customers = (await db.scalar(select(func.count()).select_from(User).where(User.role == UserRole.CUSTOMER))) or 0
    # Growth: last 30 days vs previous 30
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    d30 = now - timedelta(days=30)
    d60 = now - timedelta(days=60)
    recent_orders = (await db.scalar(select(func.count()).select_from(Order).where(Order.created_at >= d30))) or 0
    prev_orders = (await db.scalar(select(func.count()).select_from(Order).where(Order.created_at >= d60, Order.created_at < d30))) or 0
    growth = round(((recent_orders - prev_orders)/prev_orders*100) if prev_orders else (100 if recent_orders else 0), 1)
    return ApiResponse(status=200, message="Overview", data={
        "totalOrders": total_orders,
        "totalRevenue": float(total_revenue),
        "totalProducts": total_products,
        "totalCustomers": total_customers,
        "growthRate": growth,
        "recentOrders": recent_orders,
    })

@router.get("/revenue-chart", status_code=status.HTTP_200_OK)
async def revenue_chart(days: int = Query(7, ge=1, le=90), db: AsyncSession = Depends(db_session), admin: User = Depends(get_current_admin)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    data = []
    for i in range(days-1, -1, -1):
        day = (now - timedelta(days=i)).date()
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        rev = await db.scalar(select(func.coalesce(func.sum(Order.total_price), 0)).where(Order.created_at >= start, Order.created_at <= end, Order.status != OrderStatus.CANCELLED))
        cnt = await db.scalar(select(func.count()).select_from(Order).where(Order.created_at >= start, Order.created_at <= end))
        data.append({"date": str(day), "revenue": float(rev or 0), "orders": cnt or 0})
    return ApiResponse(status=200, message="Revenue chart", data=data)

@router.get("/top-products", status_code=status.HTTP_200_OK)
async def top_products(limit: int = 5, db: AsyncSession = Depends(db_session), admin: User = Depends(get_current_admin)):
    # Simplified: top by stock movement; fallback to newest
    stmt = select(Product).order_by(Product.stock_quantity.desc()).limit(limit)
    result = await db.scalars(stmt)
    products = list(result.all())
    return ApiResponse(status=200, message="Top products", data=[{"id": p.id, "name": p.name, "price": float(p.price), "stock": p.stock_quantity, "image": p.image_url} for p in products])
