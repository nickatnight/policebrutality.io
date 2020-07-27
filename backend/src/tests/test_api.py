import falcon

from src.app import VERSION
from src.services.link_service import LinkService
from src.services.video_service import VideoService
from src.tests.utils import BaseTestCase


class APITestCase(BaseTestCase):
    def test_ping_ok(self):
        """test health edpoint returns 200 when available
        """
        response = self.simulate_get(f"/{VERSION}/ping")
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"pong": "OK"})

    def test_videos_empty(self):
        """test count is 0 and data is empty list when no data
        """
        response = self.simulate_get(f"/{VERSION}/videos")
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"count": 0, "data": []})

    def test_videos_not_empty(self):
        """test count is 1 and data contains 1 instance
        """
        v = {
            "state": "California",
            "city": "San Diego",
            "edit_at": "meh",
            "date": "2020-06-01",
            "date_text": "June 1st",
            "pbid": "ca-sandiego-1",
            "description": "test test",
        }
        video = VideoService.create_video(**v)
        LinkService.create_link(
            video,
            {
                "url": "http://shitpissfuckcuntcocksuckermotherfuckertitsfartterdandtwat.com",
                "text": "",
            },
        )
        response = self.simulate_get(f"/{VERSION}/videos")
        self.assertEqual(response.status, falcon.HTTP_OK)
        print(response.json)
        self.assertEqual(
            response.json,
            {
                "count": 1,
                "data": [
                    {
                        "id": "ca-sandiego-1",
                        "edit_at": "meh",
                        "date": "2020-06-01",
                        "date_text": "June 1st",
                        "name": None,
                        "state": "California",
                        "description": "test test",
                        "city": "San Diego",
                        "tags": [],
                        "links": [
                            {
                                "key": None,
                                "link": "http://shitpissfuckcuntcocksuckermotherfuckertitsfartterdandtwat.com",  # noqa
                                "spaces_url": "",
                                "text": None,
                            }
                        ],
                    }
                ],
            },
        )
