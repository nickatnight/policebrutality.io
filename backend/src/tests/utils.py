from falcon import testing
from mongoengine import connect, disconnect

from src import app


class BaseTestCase(testing.TestCase):
    API_DATA = {
        "edit_at": "https://github.com/2020PB/police-brutality",
        "help": "ask @ubershmekel on twitter",
        "updated_at": "2020-06-14T03:12:16.963848+00:00",
        "data": [
            {
                "links": [
                    "https://twitter.com/courtenay_roche/status/1267653137969623040",
                    "https://twitter.com/yagirlbrookie09/status/1267647898365427714",
                    "https://www.4029tv.com/article/bentonville-police-deploy-tear-gas-on-protesters/32736629#",  # noqa
                ],
                "state": "Arkansas",
                "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",  # noqa
                "city": "Bentonville",
                "name": "Law enforcement gas a crowd chanting \u201cwe want peace\u201d right after exiting the building.",  # noqa
                "date": "2020-06-01",
                "date_text": "June 1st",
                "id": "ar-bentonville-1",
            },
            {
                "links": [
                    "https://twitter.com/KATVShelby/status/1267554421019475972",
                    "https://twitter.com/KATVNews/status/1267509911954440194",
                ],
                "state": "Arkansas",
                "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",  # noqa
                "city": "Little Rock",
                "name": "Peaceful protestors kneeling are shot with an explosive projectile.",
                "date": "2020-05-31",
                "date_text": "May 31st",
                "id": "ar-littlerock-1",
            },
        ],
    }

    def setUp(self):
        super().setUp()
        self.app = app.initialize()

    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://mongodb:27017", alias="default")

    @classmethod
    def tearDownClass(cls):
        disconnect()
