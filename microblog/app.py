from flask import Flask
from . import frontend
from . import extensions

__all__ = ["create_app"]


def create_app(app_name):
    app = Flask(app_name)
    app.config.from_object("microblog.config")
    configure_blueprints(app)
    configure_extensions(app)
    return app


def configure_blueprints(app):
    app.register_blueprint(frontend.index_bp)
    app.register_blueprint(frontend.login_bp)


def configure_extensions(app):
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)