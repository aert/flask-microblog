from flask import Blueprint, flash, redirect, url_for, render_template, g
from flask.ext.login import login_required
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required, Length
from microblog.extensions import db
from microblog.models import User


user_bp = Blueprint('user', __name__)


# --- Forms -------------------------------------------------------------------

class EditForm(Form):
    nickname = TextField('nickname', validators=[Required()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        nickname_exists = User.check_nickname_exists(self.nickname.data)
        if nickname_exists:
            self.nickname.errors.append('This nickname is already in use.'
                                        'Please choose another one.')
            return False
        return True


# --- Controllers -------------------------------------------------------------

@user_bp.route('/<nickname>')
@login_required
def user(nickname):
    user_found = User.query.filter_by(nickname=nickname).first()
    if user_found is None:
        flash('User %s not found.' % nickname, "danger")
        return redirect(url_for('index.home'))
    posts = [
        {'author': user_found, 'body': 'Test post #1'},
        {'author': user_found, 'body': 'Test post #2'},
    ]
    return render_template('frontend/user.html',
                           title='User',
                           user=user_found,
                           posts=posts)


@user_bp.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.', "success")
        return redirect(url_for('user.user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
        return render_template('frontend/user_edit.html',
                               title="User Edit",
                               form=form)


@user_bp.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user_found = User.query.filter_by(nickname=nickname).first()
    if user_found is None:
        flash('User %s not found.' % nickname, "danger")
        return redirect(url_for('index.home'))
    if user_found == g.user:
        flash('You can\'t follow youself !', "warning")
        return redirect(url_for('user.user', nickname=nickname))
    u = g.user.follow(user_found)
    if u is None:
        flash('You already follow %s.' % nickname)
        return redirect(url_for('user.user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following %s.' % nickname, "success")
    return redirect(url_for('user.user', nickname=nickname))


@user_bp.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user_found = User.query.filter_by(nickname=nickname).first()
    if user_found is None:
        flash('User %s not found.' % nickname, "danger")
        return redirect(url_for('index.home'))
    if user_found == g.user:
        flash('You can\'t unfollow youself !', "warning")
        return redirect(url_for('user.user', nickname=nickname))
    u = g.user.unfollow(user_found)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.', "warning")
        return redirect(url_for('user.user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.', "success")
    return redirect(url_for('user.user', nickname=nickname))
