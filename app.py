import logging
from flask import Flask

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


@app.route("/")
def hello() -> str:
    return "Hello, World!"


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
