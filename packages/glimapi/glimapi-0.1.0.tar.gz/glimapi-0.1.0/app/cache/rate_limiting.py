from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from starlette.responses import JSONResponse
import time

class InMemoryLimiter:
    """
    A simple in-memory rate limiter to be used when Redis is not available.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.clients = {}

    async def __call__(self, request: Request, call_next):
        client_id = request.client.host
        client_info = self.clients.get(client_id, {"count": 0, "expires": 0})
        current_time = int(time.time())

        if client_info["expires"] < current_time:
            client_info = {"count": 1, "expires": current_time + self.window_seconds}
        else:
            client_info["count"] += 1

        if client_info["count"] > self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)

        self.clients[client_id] = client_info
        response = await call_next(request)
        return response

def setup_rate_limiting(settings, app: FastAPI):
    """
    Set up the rate limiting middleware.

    This function will initialize the FastAPILimiter with the Redis connection if enabled,
    or use an in-memory rate limiter if Redis is not enabled.

    Args:
        settings (app.config.Settings): The settings of the application.
        app (fastapi.FastAPI): The FastAPI application.
    """
    if settings.cache.get("enabled", False):  # Check if Redis is enabled in the config
        redis = app.state.cache
        FastAPILimiter.init(redis)
        rate_limiter_dependency = RateLimiter(
            times=settings.rate_limiting["max_requests_per_minute"], 
            seconds=60
        )
        app.dependency_overrides[RateLimiter] = rate_limiter_dependency
    else:
        # Use the in-memory rate limiter if Redis is not enabled
        in_memory_limiter = InMemoryLimiter(
            max_requests=settings.rate_limiting["max_requests_per_minute"],
            window_seconds=60
        )
        app.middleware("http")(in_memory_limiter)  # Middleware added here
