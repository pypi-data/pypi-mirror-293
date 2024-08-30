import redis.asyncio as redis
from starlette.middleware.cors import CORSMiddleware

def setup_cache(settings, app):
    """
    Set up the Redis cache for the application.

    This function will create a connection to the Redis server and store it in the app's state.

    Args:
        settings (app.config.Settings): The settings of the application.
        app (fastapi.FastAPI): The FastAPI application.
    """
    # Create a connection to the Redis server using redis-py
    redis_client = redis.from_url(f"redis://{settings.cache['host']}:{settings.cache['port']}")

    # Store the connection in the app's state
    app.state.cache = redis_client

    # Enable CORS for the application
    app.add_middleware(
        CORSMiddleware,
        # Allow requests from all origins
        allow_origins=["*"],
        # Allow the client to specify cookies
        allow_credentials=True,
        # Allow all methods
        allow_methods=["*"],
        # Allow all headers
        allow_headers=["*"],
    )
