from unittest import mock

from src.utils.github import GitHubAPI
from src.utils.helpers import RequestAPI
from src.models.link import Link
from src.models.video import Video
from src.tests.utils import BaseTestCase


class GitHubTestCase(BaseTestCase):
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


class HelpersTestCase(BaseTestCase):
    def test_request_api_get(self):
        """test RequestAPI returns 200
        """
        api = RequestAPI()
        resp = api.request("http://backend:5000/v1/ping")
        self.assertEqual(resp.status_code, 200)
