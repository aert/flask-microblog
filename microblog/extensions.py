from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy


# SQLAlchemy
db = SQLAlchemy()

# Flask-Migrate
migrate = Migrate()