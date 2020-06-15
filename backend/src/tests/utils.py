from falcon import testing
from mongoengine import connect, disconnect

from src import app


class BaseTestCase(testing.TestCase):
    def setUp(self):
        super().setUp()
        self.app = app.initialize()

    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://mongodb:27017", alias="default")

    @classmethod
    def tearDownClass(cls):
        disconnect()
