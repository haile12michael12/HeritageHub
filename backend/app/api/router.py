from fastapi import APIRouter
from .auth import router as auth_api
from .users import router as users_api
from .category import router as category_api
from .product import router as product_api
from .cart import router as cart_api
from .order import router as order_api
from .payment import router as payment_api
from .review import router as review_api
from .report import router as report_api
from .wishlist import router as wishlist_api
from .coupon import router as coupon_api
from .search import router as search_api
from .notifications_ws import router as notifications_api
from .analytics import router as analytics_api

api_router = APIRouter()


@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "HeritageHub API",
        "version": "2.0.0",
        "features": ["auth", "products", "cart", "orders", "payments", "wishlist", "coupons", "search", "analytics", "realtime"]
    }


api_router.include_router(auth_api)
api_router.include_router(users_api)
api_router.include_router(category_api)
api_router.include_router(product_api)
api_router.include_router(cart_api)
api_router.include_router(order_api)
api_router.include_router(payment_api)
api_router.include_router(review_api)
api_router.include_router(report_api)
api_router.include_router(wishlist_api)
api_router.include_router(coupon_api)
api_router.include_router(search_api)
api_router.include_router(notifications_api)
api_router.include_router(analytics_api)
