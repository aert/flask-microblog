from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy


# SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()

# Flask-Login
lm = LoginManager()

# Flask-OpenID
oid = OpenID()