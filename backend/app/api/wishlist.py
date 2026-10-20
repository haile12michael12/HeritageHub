from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import db_session
from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.response import ApiResponse
from app.schemas.wishlist import WishlistAdd
from app.services.wishlist_service import get_wishlist, add_to_wishlist, remove_from_wishlist

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.get("", status_code=status.HTTP_200_OK)
async def list_wishlist(db: AsyncSession = Depends(db_session), user: User = Depends(get_current_user)):
    items = await get_wishlist(db, user.id)
    return ApiResponse(status=200, message="Wishlist retrieved", data=items)

@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_item(req: WishlistAdd, db: AsyncSession = Depends(db_session), user: User = Depends(get_current_user)):
    await add_to_wishlist(db, user.id, req.product_id)
    return ApiResponse(status=201, message="Added to wishlist")

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def remove_item(product_id: int, db: AsyncSession = Depends(db_session), user: User = Depends(get_current_user)):
    await remove_from_wishlist(db, user.id, product_id)
    return ApiResponse(status=200, message="Removed from wishlist")
