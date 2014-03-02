import datetime
from flask import Blueprint, g, render_template
from flask.ext.login import current_user
from microblog.extensions import db


global_bp = Blueprint("global", __name__)


@global_bp.before_app_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@global_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@global_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
