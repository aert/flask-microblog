from os.path import join
from flask import Flask
from . import frontend
from . import extensions

__all__ = ["create_app"]


def create_app():
    app = Flask(__name__)
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

    extensions.lm.init_app(app)
    extensions.lm.login_view = 'login.login'
    extensions.oid.init_app(app)
    extensions.oid.fs_store_path = join(app.config["DATADIR"], 'tmp')
