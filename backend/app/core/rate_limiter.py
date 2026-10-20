import time
from collections import defaultdict, deque
from fastapi import Request
from fastapi.responses import JSONResponse

class InMemoryRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.clients: dict[str, deque] = defaultdict(deque)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        q = self.clients[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.max_requests:
            return False
        q.append(now)
        return True

    def retry_after(self, key: str) -> int:
        q = self.clients[key]
        if not q:
            return 0
        return int(self.window - (time.time() - q[0])) + 1

limiter = InMemoryRateLimiter(max_requests=100, window_seconds=60)
strict_limiter = InMemoryRateLimiter(max_requests=5, window_seconds=60)

async def rate_limit_middleware(request: Request, call_next):
    # Skip health/docs
    if request.url.path in ("/health", "/docs", "/openapi.json", "/api/health"):
        return await call_next(request)
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{request.url.path}"
    # Use strict limiter for auth endpoints
    current_limiter = strict_limiter if "/auth/" in request.url.path else limiter
    if not current_limiter.is_allowed(key):
        return JSONResponse(
            status_code=429,
            content={"status": 429, "message": f"Too many requests. Retry after {current_limiter.retry_after(key)}s", "data": None},
            headers={"Retry-After": str(current_limiter.retry_after(key))}
        )
    return await call_next(request)
