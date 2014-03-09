from os.path import join
from flask import Flask, current_app
from . import frontend
from . import extensions
from .config import create_dirs
from . import models                 # NOQA
from flask.ext import whooshalchemy  # NOQA


__all__ = ["create_app"]


def create_app(settings_override=None):
    """Returns a :class:`Flask` application instance configured with common
    functionality.

    :param settings_override: a dictionary of settings to override
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object("microblog.config")
    app.config.from_envvar('MICROBLOG_SETTINGS', silent=True)
    app.config.from_object(settings_override)

    create_dirs(app.config['WORKINGDIR'])
    create_dirs(app.config['LOGDIR'])
    create_dirs(app.config['WHOOSH_BASE'])

    configure(app)

    app.before_first_request(before_first_request)

    return app


def configure(app):
    configure_blueprints(app)
    configure_extensions(app)
    app.logger.info('microblog initialized')


def configure_logging(app):
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler

        create_dirs(app.config['LOGDIR'])

        file_handler = RotatingFileHandler(
            join(app.config['LOGDIR'], 'microblog.log'),
            'a', 1 * 1024 * 1024,
            10
        )
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

    # DB
    extensions.db.init_app(app)
    extensions.migrate.init_app(app, extensions.db)

    # WHOOSH
    #whooshalchemy.whoosh_index(app, models.Post)

    # Login
    extensions.lm.init_app(app)
    extensions.lm.login_view = 'login.login'

    # OID
    extensions.oid.init_app(app)
    extensions.oid.fs_store_path = app.config['OID_FS_STORE_PATH']


def before_first_request():
    configure_logging(current_app)
    current_app.logger.info('before_first_request')

    # SENTRY
    if not current_app.debug:
        extensions.sentry.init_app(current_app,
                                   dsn=current_app.config['SENTRY_DSN'])
