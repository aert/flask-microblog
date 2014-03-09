import flask
from flask import Blueprint, render_template, flash, g, url_for, session, \
    request, current_app
from flask.ext.login import login_user, logout_user
from flask.ext.wtf import Form
from flask.ext.babel import gettext as _
from werkzeug.utils import redirect
from wtforms import TextField, BooleanField
from wtforms.validators import Required
from microblog.extensions import lm, oid, db
from microblog.models import User, ROLE_USER


login_bp = Blueprint("login", __name__, template_folder="templates")


# --- Forms -------------------------------------------------------------------

class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=None)


# --- Controllers -------------------------------------------------------------

class Mock(object):
    pass


@login_bp.route("/testing-login", methods=["POST"])
def testing_login():
    if not current_app.config['TESTING']:
        raise Exception("NOT IN TESTING MODE")

    form = LoginForm()

    #if not form.validate_on_submit():
    #    raise Exception("validate_on_submit = False!")

    resp = Mock()
    resp.email = form.openid.data
    resp.nickname = None
    return after_login(resp)


@login_bp.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index.home'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template(
        "frontend/login.html",
        title=_("Sign In"),
        form=form,
        providers=flask.current_app.config['OPENID_PROVIDERS'])


@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.home'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash(_('Invalid login. Please try again.'), "danger")
        return redirect(url_for('.login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email, role=ROLE_USER)
        db.session.add(user)
        db.session.commit()
        # make the user follow him/herself
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember_me)
    return redirect(request.args.get('next') or url_for('index.home'))


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
