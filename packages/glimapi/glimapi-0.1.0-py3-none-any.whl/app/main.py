from fastapi import FastAPI, Request
from app.config import settings
from app.db.database import MongoDBConnector
from app.model.models import generate_apis
from app.auth.auth import AuthMiddleware
from app.cache.cache import setup_cache
from app.cache.rate_limiting import setup_rate_limiting
from datetime import datetime
import importlib.util
import os
import uvicorn
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from fastapi import FastAPI, Request, HTTPException
import logging
import uvicorn
import shutil

logging.basicConfig(level=logging.WARNING)

app = FastAPI(debug=settings.server["debug"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"An unexpected error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def custom_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."}
    )


@app.exception_handler(StarletteHTTPException)
async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logging.error(f"Starlette HTTP error occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Connect to the MongoDB database
mongodb_connector = MongoDBConnector(settings)

# If JWT authentication is enabled, add the authentication middleware
if settings.auth["jwt_enabled"]:
    app.middleware("http")(AuthMiddleware(settings))

# If caching is enabled, set up the cache middleware
if settings.cache["enabled"]:
    setup_cache(settings, app)

# Set up rate limiting middleware (Redis-based or In-memory)
if settings.rate_limiting["enabled"]:
    setup_rate_limiting(settings, app)

# Load custom middleware modules from the "middlewares" directory
target_copy_dir = os.path.join(os.getcwd(), "middlewares")
for filename in os.listdir(target_copy_dir):
    if filename.endswith(".py"):
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(target_copy_dir, filename))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        async def wrapped_middleware(request: Request, call_next):
            try:
                return await module.custom_middleware(request, call_next)
            except HTTPException as exc:
                return JSONResponse(
                    status_code=exc.status_code,
                    content={"detail": exc.detail}
                )
            except Exception as exc:
                return JSONResponse(
                    status_code=500,
                    content={"detail": "An internal server error occurred."}
                )

        app.middleware("http")(wrapped_middleware)


# Generate the API endpoints
generate_apis(app, mongodb_connector)

def run():
    """
        This is the main entry point of the application.

        This script will start the FastAPI application using Uvicorn.

        If the script is run directly (not imported), it will start a development server
        with the following configuration:

        - host: settings.server.host
        - port: settings.server.port
    """
    uvicorn.run(app, host=settings.server["host"], port=settings.server["port"], log_level="info")

if __name__ == "__main__":
    run()