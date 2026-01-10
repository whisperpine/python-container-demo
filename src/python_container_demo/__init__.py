import logging

import uvicorn

from .server import app


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=False)
