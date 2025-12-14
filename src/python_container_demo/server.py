import logging
from fastapi import FastAPI, HTTPException

# All standard HTTP methods.
ALL_METHODS: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]

# Initialize the logger.
logger: logging.Logger = logging.getLogger(__name__)

# Initializes FastAPI.
app = FastAPI()


@app.api_route("/", methods=["GET"])
async def hello() -> str:
    return "Hello, World!"


@app.api_route("/echo/{phrase}", methods=["GET"])
async def echo(phrase: str) -> str:
    return phrase


@app.api_route("/{full_path:path}", methods=ALL_METHODS)
async def fallback_handler(full_path: str):
    """
    Catch-all fallback for unmatched routes.

    Args:
        full_path: the full url path from an http request.
    """
    raise HTTPException(
        status_code=404,
        detail=f"Path '/{full_path}' not found.",
    )
