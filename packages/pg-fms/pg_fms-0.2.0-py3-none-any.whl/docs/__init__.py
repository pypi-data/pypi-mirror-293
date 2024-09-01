from flask import Flask
import logging
from requests import get, ConnectionError
import sys
import os


def create_app():
    """Construct the core application."""
    app = Flask(__name__, template_folder="templates")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    with app.app_context():
        from src.docs import routes

        app.add_url_rule("/", view_func=routes.landing_page)
        app.add_url_rule("/<path:subpath>", view_func=routes.catch_all)

        return app
