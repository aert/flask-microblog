from flask.ext.babel import Babel
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry


# SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()

# Flask-Login
lm = LoginManager()

# Flask-OpenID
oid = OpenID()

# Sentry
sentry = Sentry()

# Flask-Babel
babel = Babel()
