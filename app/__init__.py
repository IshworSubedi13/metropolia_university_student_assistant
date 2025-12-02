import os

from flask import Flask
from flask_cors import CORS


def create_app():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
    CORS(app)

    from .routes.chat import chat_bp

    app.register_blueprint(chat_bp)
    return app
