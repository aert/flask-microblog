import tempfile
import unittest
from os.path import join
from microblog.factory import create_app
from microblog.extensions import db


class TestConfig(object):
    LOGIN_DISABLED = False
    TESTING = True
    CSRF_ENABLED = False,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % join(tempfile.gettempdir(),
                                                    "microblog_test.db")


class BaseTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig())
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, openid):
        return self.client.post('/testing-login', data=dict(
            openid=openid,
            remember_me=""
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)
