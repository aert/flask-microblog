import datetime
from flask import Blueprint, g, render_template, redirect, url_for
from flask.ext.login import current_user, login_required
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required
from microblog.config import MAX_SEARCH_RESULTS
from microblog.extensions import db
from microblog.lib.locale import get_locale
from microblog.models import Post


global_bp = Blueprint("global", __name__)


# --- Forms -------------------------------------------------------------------

class SearchForm(Form):
    search = TextField('search', validators=[Required()])


# --- Controllers -------------------------------------------------------------

@global_bp.before_app_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()


@global_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), error


@global_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), error


@global_bp.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index.home'))
    return redirect(url_for('.search_results',
                            query=g.search_form.search.data))


@global_bp.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('frontend/search_results.html',
                           query=query,
                           results=results)
