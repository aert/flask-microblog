from os.path import join
from types import MethodType
from flask import Flask
from . import frontend
from . import extensions

__all__ = ["create_app"]


def create_app():
    app = Flask(__name__)
    app.config.from_object("microblog.config")
    app.configure = MethodType(configure, app)
    configure_db(app)
    return app


def configure(app):
    configure_logging(app)
    configure_blueprints(app)
    configure_extensions(app)
    app.db = extensions.db
    app.logger.info('microblog initialized')


def configure_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('tmp/microblog.log',
                                           'a', 1 * 1024 * 1024,
                                           10)
        fmt = '%(asctime)s %(levelname)s: %(message)s '\
              '[in %(pathname)s:%(lineno)d]'
        file_handler.setFormatter(logging.Formatter(fmt))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('microblog initializing')


def configure_blueprints(app):
    app.logger.info('configure_blueprints')
    app.register_blueprint(frontend.global_bp)
    app.register_blueprint(frontend.index_bp)
    app.register_blueprint(frontend.login_bp)
    app.register_blueprint(frontend.user_bp, url_prefix='/user')


def configure_extensions(app):
    app.logger.info('configure_extensions')
    if not app.debug:
        extensions.sentry.init_app(app, dsn=app.config['SENTRY_DSN'])

    extensions.lm.init_app(app)
    extensions.lm.login_view = 'login.login'
    extensions.oid.init_app(app)
    extensions.oid.fs_store_path = join(app.config["DATADIR"], 'tmp')


def configure_db(app):
    app.logger.info('configure_db')
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)
