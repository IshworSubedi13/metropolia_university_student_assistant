import logging

from flask import send_from_directory

from app import create_app
from app.config import config

app = create_app()
logger = logging.getLogger(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def index(path):
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    logger.info(
        "Starting Student Assistant AI backend (Gemini) on port %s",
        config.PORT
    )
    app.run(host="0.0.0.0", port=config.PORT, debug=True)
