from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import db_session
from app.models.product import Product
from app.models.category import Category
from app.schemas.response import ApiResponse
from app.core.pagination import paginate_params

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("", status_code=status.HTTP_200_OK)
async def search_products(
    q: Optional[str] = Query(None, description="Search term"),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = Query("newest", enum=["newest", "price_asc", "price_desc", "name", "popular"]),
    page: int = 1,
    page_size: int = 12,
    db: AsyncSession = Depends(db_session),
):
    page, page_size, offset = paginate_params(page, page_size)
    base = select(Product)
    count_stmt = select(func.count()).select_from(Product)
    filters = []
    if q:
        like = f"%{q}%"
        filters.append(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if category_id:
        filters.append(Product.category_id == category_id)
    if min_price is not None:
        filters.append(Product.price >= min_price)
    if max_price is not None:
        filters.append(Product.price <= max_price)
    for f in filters:
        base = base.where(f)
        count_stmt = count_stmt.where(f)
    total = (await db.scalar(count_stmt)) or 0
    # Sorting
    if sort_by == "price_asc":
        base = base.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        base = base.order_by(Product.price.desc())
    elif sort_by == "name":
        base = base.order_by(Product.name.asc())
    elif sort_by == "popular":
        base = base.order_by(Product.stock_quantity.desc())
    else:
        base = base.order_by(Product.created_at.desc())
    base = base.offset(offset).limit(page_size)
    result = await db.scalars(base)
    products = list(result.all())
    # Trending categories
    return ApiResponse(
        status=200,
        message="Search results",
        data={
            "items": products,
            "total": total,
            "page": page,
            "pageSize": page_size,
            "totalPages": (total + page_size - 1)//page_size if total else 1,
        },
    )

@router.get("/suggestions", status_code=status.HTTP_200_OK)
async def search_suggestions(q: str = Query(..., min_length=1), db: AsyncSession = Depends(db_session)):
    like = f"%{q}%"
    stmt = select(Product.name).where(Product.name.ilike(like)).limit(5)
    result = await db.scalars(stmt)
    return ApiResponse(status=200, message="Suggestions", data=list(result.all()))

@router.get("/trending", status_code=status.HTTP_200_OK)
async def trending_products(db: AsyncSession = Depends(db_session)):
    stmt = select(Product).order_by(Product.created_at.desc()).limit(8)
    result = await db.scalars(stmt)
    return ApiResponse(status=200, message="Trending products", data=list(result.all()))
