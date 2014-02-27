import flask
from flask import Blueprint, render_template, flash
from flask_wtf import Form
from werkzeug.utils import redirect
from wtforms import TextField, BooleanField
from wtforms.validators import Required


login_bp = Blueprint("login", __name__, template_folder="templates")


class LoginForm(Form):
    openid = TextField('openid', validators=[Required()])
    remember_me = BooleanField('remember_me', default=None)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template("frontend/login.html",
                           title="Sign In",
                           form=form,
                           providers=flask.current_app.config['OPENID_PROVIDERS'])