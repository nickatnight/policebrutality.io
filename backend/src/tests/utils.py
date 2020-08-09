from unittest import mock

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
                    {
                        "url": "https://twitter.com/courtenay_roche/status/1267653137969623040",
                        "text": "",
                    },
                    {
                        "url": "https://twitter.com/yagirlbrookie09/status/1267647898365427714",
                        "text": "",
                    },
                    {
                        "url": "https://www.4029tv.com/article/bentonville-police-deploy-tear-gas-on-protesters/32736629#",  # noqa
                        "text": "",
                    },
                ],
                "state": "Arkansas",
                "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",  # noqa
                "city": "Bentonville",
                "name": "Law enforcement gas a crowd chanting \u201cwe want peace\u201d right after exiting the building.",  # noqa
                "date": "2020-06-01",
                "date_text": "June 1st",
                "id": "ar-bentonville-1",
                "description": "Danger",
                "tags": ["arrest", "pepper-spray", "spray"],
            },
            {
                "links": [
                    {
                        "url": "https://twitter.com/KATVShelby/status/1267554421019475972",
                        "text": "",
                    },
                    {
                        "url": "https://twitter.com/KATVNews/status/1267509911954440194",
                        "text": "",
                    },
                ],
                "state": "Arkansas",
                "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",  # noqa
                "city": "Little Rock",
                "name": "Peaceful protestors kneeling are shot with an explosive projectile.",
                "date": "2020-05-31",
                "date_text": "May 31st",
                "id": "ar-littlerock-1",
                "description": "Ranger",
                "tags": ["tackle", "strike", "knee", "spray",],
            },
        ],
    }

    def _mock_response(
        self, status=200, content="CONTENT", json_data=None, raise_for_status=None
    ):
        """
        since we typically test a bunch of different
        requests calls for a service, we are going to do
        a lot of mock responses
        """
        mock_resp = mock.Mock()
        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()
        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content
        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(return_value=json_data)
        return mock_resp

    def setUp(self):
        super().setUp()
        self.app = app.initialize()

    @classmethod
    def setUpClass(cls):
        connect("mongoenginetest", host="mongomock://mongodb:27017", alias="default")

    @classmethod
    def tearDownClass(cls):
        disconnect()
