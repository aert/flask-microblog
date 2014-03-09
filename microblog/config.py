# coding=utf-8
from os.path import join, abspath, dirname, isdir
from os import makedirs


def create_dirs(*directories):
    for dirpath in directories:
        if not isdir(dirpath):
            makedirs(dirpath)


BASEDIR = abspath(dirname(__file__))
WORKINGDIR = join(dirname(BASEDIR), "working")
LOGDIR = join(WORKINGDIR, "log")


# Flask-WTF
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# OpenID
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]
OID_FS_STORE_PATH = join(WORKINGDIR, "oid")

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(WORKINGDIR, 'database.db')

# Sentry
SENTRY_DSN = 'http://164bac68585941efa0ba10a3e33a634a:' \
             '8c9e30a2c9104c359fe67e0147490704@sentry.aert.fr/3'

# Pagination
POST_PER_PAGE = 3

# flask-whooshalchemy
WHOOSH_BASE = join(WORKINGDIR, "whoosh")
MAX_SEARCH_RESULTS = 50

# Babel
LANGUAGES = {
    'en': 'English',
    'fr': 'Français'
}
