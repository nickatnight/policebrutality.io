import falcon
from falcon import testing
from mongoengine import connect, disconnect
# import pytest

from src import app
# from src import settings


# @pytest.fixture
# def client():
#     return testing.TestClient(app)


class BaseTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()
        self.app = app.initialize()

    @classmethod
    def setUpClass(cls):
        connect('mongoenginetest', host='mongomock://mongodb:27017', alias='default')

    @classmethod
    def tearDownClass(cls):
        disconnect()
