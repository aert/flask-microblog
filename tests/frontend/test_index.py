from tests.base import BaseTest


class TestIndex(BaseTest):

    def test_home_without_auth(self):
        response = self.client.get('/')
        assert "Redirecting..." in response.data

    def test_home_with_auth(self):
        self.login("hello@gmail.com")
        response = self.client.get('/')
        assert "Index" in response.data
