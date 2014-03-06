from datetime import datetime
from flask import Blueprint, g, flash, redirect, url_for
from flask import render_template
from flask.ext.login import login_required
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required
from microblog.extensions import db
from microblog.models import Post


index_bp = Blueprint("index", __name__, template_folder="templates")


# --- Forms -------------------------------------------------------------------

class PostForm(Form):
    post = TextField('post', validators=[Required()])


# --- Controllers -------------------------------------------------------------

@index_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(),
                    author=g.user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('.home'))

    posts = g.user.followed_posts().all()
    return render_template("frontend/index.html",
                           title="Home",
                           form=form,
                           posts=posts)
