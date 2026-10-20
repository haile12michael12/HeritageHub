from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.db.database import engine
from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import ApiException, api_exception_handler
from app.core.rate_limiter import rate_limit_middleware
from app.middleware.request_id import RequestIDMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Attempting to connect to DB...")
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        print(f"✅ DB Connection successful: {settings.DATABASE_URL}")
    except Exception as e:
        print(f"⚠️ DB Connection warning: {e} (continuing without DB for demo)")
    yield
    print("🔄 Closing DB connection pool...")
    try:
        await engine.dispose()
    except:
        pass
    print("✅ Closed.")

app = FastAPI(
    title="HeritageHub API",
    version="2.0.0",
    description="Professional multi-vendor e-commerce platform with AI, real-time, and analytics",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Authentication", "description": "Auth & OAuth"},
        {"name": "Products", "description": "Product catalog with search & filters"},
        {"name": "Cart", "description": "Shopping cart operations"},
        {"name": "Orders", "description": "Order lifecycle management"},
        {"name": "Payments", "description": "Stripe & local gateways"},
        {"name": "Wishlist", "description": "User wishlist"},
        {"name": "Coupons", "description": "Promotions & discounts"},
        {"name": "Search", "description": "Advanced search & suggestions"},
        {"name": "Analytics", "description": "Revenue & performance metrics"},
        {"name": "Notifications", "description": "Real-time notifications via WebSocket"},
    ],
)

# Middleware stack
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_rate_limit(request: Request, call_next):
    return await rate_limit_middleware(request, call_next)

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": "HeritageHub API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health",
        "frontend": settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else "http://localhost:5173"
    }

@app.get("/hello", tags=["Root"])
async def say_hello():
    return {"message": "Hello from HeritageHub 👋", "version": "2.0.0"}

@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok", "service": "heritagehub", "version": "2.0.0"}

app.add_exception_handler(ApiException, api_exception_handler)
app.include_router(api_router, prefix="/api")
