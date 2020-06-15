from unittest import mock

from requests.exceptions import HTTPError

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

    @mock.patch("src.utils.helpers.requests.get")
    def test_github_get_all_locations_data(self, mock_requests_get):
        """test calling get_all_locations_data() returns expected data
        """
        mock_resp = self._mock_response(status=200, json_data={"data": []})
        mock_requests_get.return_value = mock_resp
        handler = GitHubAPI()
        data = handler.get_all_locations_data()
        self.assertEqual(data, {"data": []})


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
