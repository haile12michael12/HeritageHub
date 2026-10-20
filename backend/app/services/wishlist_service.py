from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import status
from app.core.exceptions import ApiException
from app.models.wishlist import Wishlist
from app.models.product import Product

async def get_wishlist(db: AsyncSession, user_id: int):
    stmt = select(Wishlist).where(Wishlist.user_id == user_id).options(selectinload(Wishlist.product))
    result = await db.scalars(stmt)
    items = result.all()
    return [
        {
            "id": w.id,
            "product_id": w.product_id,
            "product_name": w.product.name if w.product else None,
            "product_price": w.product.price if w.product else None,
            "product_image": w.product.image_url if w.product else None,
            "created_at": w.created_at,
        }
        for w in items
    ]

async def add_to_wishlist(db: AsyncSession, user_id: int, product_id: int):
    product = await db.get(Product, product_id)
    if not product:
        raise ApiException("Product not found", status.HTTP_404_NOT_FOUND)
    existing = await db.scalar(select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id))
    if existing:
        raise ApiException("Already in wishlist", status.HTTP_400_BAD_REQUEST)
    w = Wishlist(user_id=user_id, product_id=product_id)
    db.add(w)
    await db.commit()
    await db.refresh(w)
    return w

async def remove_from_wishlist(db: AsyncSession, user_id: int, product_id: int):
    w = await db.scalar(select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id))
    if not w:
        raise ApiException("Not in wishlist", status.HTTP_404_NOT_FOUND)
    await db.delete(w)
    await db.commit()
    return True

async def is_in_wishlist(db: AsyncSession, user_id: int, product_id: int) -> bool:
    w = await db.scalar(select(Wishlist).where(Wishlist.user_id == user_id, Wishlist.product_id == product_id))
    return w is not None
