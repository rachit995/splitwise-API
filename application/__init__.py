from application.controllers.user import user_bp
from application.controllers.group import group_bp
from application.controllers.expense import expense_bp
from application.config import DevelopmentConfig
from flask import Flask
import logging
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)


def create_app():
    """Create Flask app."""
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing
    if app.debug or app.testing:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.ERROR)
    register_blueprint(app)
    return app


def register_blueprint(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(group_bp)
    app.register_blueprint(expense_bp)
