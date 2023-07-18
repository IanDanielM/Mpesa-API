"""
Main Application Module

This module initializes the Flask application and registers the blueprints
for different views. It loads environment variables using `python-dotenv`
and sets up necessary configurations.
"""
from typing import Type
from flask import Flask
from app.config import Config


def create_app(config_class: Type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.stk_push.views import stk
    from app.b2c.views import b2c
    from app.c2b.views import c2b

    app.register_blueprint(b2c)
    app.register_blueprint(stk)
    app.register_blueprint(c2b)

    return app
