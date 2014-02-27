from flask import Blueprint
from flask import render_template


index_bp = Blueprint("index", __name__, template_folder="templates")


@index_bp.route('/')
@index_bp.route('/index')
def home():
    user = {'nickname': 'Guest'}
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("frontend/index.html",
                           title="Home",
                           user=user,
                           posts=posts)