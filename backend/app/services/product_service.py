# app/services/product_service.py
from pathlib import Path

from fastapi import UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ApiException
from app.models.product import Product
from app.schemas.product import ProductUpdate
from app.services.category_service import get_category_by_id
from app.services.upload_service import upload_to_s3


async def create_product(
    db: AsyncSession,
    name: str,
    description: str,
    price: str,
    stock_quantity: int,
    category_id: int,
    file: UploadFile,
) -> Product:

    # First verify to be sure the category id exists
    await get_category_by_id(db, category_id)

    # Upload directory
    upload_dir = Path("uploads/products")

    # Upload image first
    image_path = await upload_to_s3(file, upload_dir)

    db_product = Product(
        name=name,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        category_id=category_id,
        image_url=image_path,
    )

    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def get_all_products(
    db: AsyncSession,
    category_id: int | None = None,
    q: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    sort_by: str | None = None,
    page: int = 1,
    page_size: int = 12,
) -> dict:
    from sqlalchemy import func, or_
    from app.core.pagination import paginate_params

    page, page_size, offset = paginate_params(page, page_size)
    statement = select(Product)
    count_stmt = select(func.count()).select_from(Product)
    filters = []
    if category_id:
        filters.append(Product.category_id == category_id)
    if q:
        like = f"%{q}%"
        filters.append(or_(Product.name.ilike(like), Product.description.ilike(like)))
    if min_price is not None:
        filters.append(Product.price >= min_price)
    if max_price is not None:
        filters.append(Product.price <= max_price)

    for f in filters:
        statement = statement.where(f)
        count_stmt = count_stmt.where(f)

    total = (await db.scalar(count_stmt)) or 0

    if sort_by == "price_asc":
        statement = statement.order_by(Product.price.asc())
    elif sort_by == "price_desc":
        statement = statement.order_by(Product.price.desc())
    elif sort_by == "name":
        statement = statement.order_by(Product.name.asc())
    else:
        statement = statement.order_by(Product.created_at.desc())

    statement = statement.offset(offset).limit(page_size)
    results = await db.scalars(statement)
    items = list(results.all())
    return {
        "items": items,
        "total": total,
        "page": page,
        "pageSize": page_size,
        "totalPages": (total + page_size - 1)//page_size if total else 1,
    }


async def get_product_by_id(db: AsyncSession, product_id: int) -> Product:
    # Use selectinload to eagerly fetch the reviews in one go
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.reviews))
    )

    product = await db.scalar(statement)

    if not product:
        raise ApiException("Product not found", status.HTTP_404_NOT_FOUND)

    return product


async def update_product(
    db: AsyncSession, update_data: ProductUpdate, file: UploadFile | None = None
) -> Product:

    print("Inside update product")

    db_product = await get_product_by_id(db, update_data.id)

    # Update text fields
    data = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in data.items():
        setattr(db_product, key, value)

    # Update image if new one provided
    if file:
        db_product.image_url = await upload_to_s3(file, Path("uploads/products"))

    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int) -> bool:
    db_product = await get_product_by_id(db, product_id)
    await db.delete(db_product)
    await db.commit()
    return True
