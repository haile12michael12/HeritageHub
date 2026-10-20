import uuid
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("heritage")

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())[:8]
        start = time.time()
        request.state.request_id = request_id
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-ms"] = f"{duration:.2f}"
        # Log structured
        logger.info(f"[{request_id}] {request.method} {request.url.path} -> {response.status_code} ({duration:.1f}ms)")
        return response
