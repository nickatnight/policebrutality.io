from unittest import mock

from requests.exceptions import HTTPError

from src.utils.github import GitHubAPI
from src.utils.helpers import RequestAPI
from src.models.link import Link
from src.models.video import Video
from src.tests.utils import BaseTestCase


class GitHubTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.API_DATA_UPDATE = {
            "edit_at": "https://github.com/2020PB/police-brutality",
            "help": "ask @ubershmekel on twitter",
            "updated_at": "2020-06-14T03:12:16.963848+00:00",
            "data": [
                {
                    "state": "Arkansas",
                    "edit_at": "https://github.com/2020PB/police-brutality/blob/master/reports/Arkansas.md",  # noqa
                    "city": "Bentonville",
                    "name": "Law enforcement gas a crowd chanting \u201cwe want peace\u201d right after exiting the building.",  # noqa
                    "date": "2020-06-01",
                    "date_text": "June 1st",
                    "id": "ar-bentonville-1",
                    "tags": ["tag1", "tag2"],
                    "description": "Updated description",
                    "links": [{"url": "htts://theannoyingsite.com", "text": "Got eem"}],
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

    @mock.patch("src.utils.github.GitHubAPI.get_all_locations_data")
    def test_github(self, mock_GitHubAPI_get_all_locations_data):
        """test calling 'all-locations.json' captures expected data (2 Video / 5 Link)
        """
        test_data = self.API_DATA.copy()
        mock_GitHubAPI_get_all_locations_data.return_value = test_data

        handler = GitHubAPI()
        handler.main()
        self.assertEqual(Video.objects.count(), 2)
        self.assertEqual(Link.objects.count(), 5)

    @mock.patch("src.utils.helpers.requests.get")
    def test_github_get_all_locations_data(self, mock_requests_get):
        """test calling get_all_locations_data() returns expected data
        """
        mock_resp = self._mock_response(status=200, json_data={"data": []})
        mock_requests_get.return_value = mock_resp
        handler = GitHubAPI()
        data = handler.get_all_locations_data()
        self.assertEqual(data, {"data": []})

    @mock.patch("src.utils.github.GitHubAPI.get_all_locations_data")
    def test_github_updates_existing_data(self, mock_GitHubAPI_get_all_locations_data):
        """test calling GitHub api updates expected data
        """
        api_data = self.API_DATA.copy()
        api_data2 = self.API_DATA_UPDATE.copy()
        mock_GitHubAPI_get_all_locations_data.return_value = api_data

        handler1 = GitHubAPI()
        handler1.main()
        v = Video.objects(pbid="ar-bentonville-1").first()

        self.assertEqual(
            ["arrest", "pepper-spray", "spray"].sort(), [t.name for t in v.tags].sort()
        )
        self.assertEqual("Danger", v.description)

        mock_GitHubAPI_get_all_locations_data.return_value = api_data2

        handler2 = GitHubAPI()
        handler2.main()

        v = Video.objects(pbid="ar-bentonville-1").first()
        links = Link.objects(video=v)

        self.assertEqual(["tag1", "tag2"].sort(), [t.name for t in v.tags].sort())
        self.assertEqual("Updated description", v.description)
        self.assertIn("htts://theannoyingsite.com", [link.link for link in links])


class HelpersTestCase(BaseTestCase):
    def test_request_api_get(self):
        """test RequestAPI returns 200
        """
        api = RequestAPI()
        resp = api.request("https://google.com")
        self.assertEqual(resp.status_code, 200)

    @mock.patch("src.utils.helpers.requests.get")
    def test_requests_returns_none_on_http_error(self, mock_requests_get):
        """test None response on HTTP error
        """
        mock_resp = self._mock_response(
            status=400, json_data={}, raise_for_status=HTTPError("Timeout")
        )
        mock_requests_get.return_value = mock_resp
        api = RequestAPI()
        resp = api.request("https://google.com")
        self.assertEqual(resp, None)

    @mock.patch("src.utils.helpers.requests.get")
    def test_requests_returns_none_on_non_http_error(self, mock_requests_get):
        """test None response on non HTTP error
        """
        mock_resp = self._mock_response(
            status=400, json_data={}, raise_for_status=ValueError("Some ValueError")
        )
        mock_requests_get.return_value = mock_resp
        api = RequestAPI()
        resp = api.request("https://google.com")
        self.assertEqual(resp, None)
