from os.path import join, abspath, dirname

BASEDIR = abspath(dirname(__file__))
DATADIR = dirname(BASEDIR)


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

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(DATADIR, 'test.db')

# Sentry
SENTRY_DSN = 'http://164bac68585941efa0ba10a3e33a634a:' \
             '8c9e30a2c9104c359fe67e0147490704@sentry.aert.fr/3'
