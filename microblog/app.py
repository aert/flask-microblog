from flask import Flask
from . import frontend

__all__ = ["create_app"]


def create_app(app_name):
    app = Flask(app_name)
    app.config.from_object("microblog.config")
    app.register_blueprint(frontend.index_bp)
    app.register_blueprint(frontend.login_bp)
    return app