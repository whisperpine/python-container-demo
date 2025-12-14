def main() -> None:
    import logging, uvicorn
    from .server import app

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=False)
