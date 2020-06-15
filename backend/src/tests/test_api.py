import falcon

from src.services.link_service import LinkService
from src.services.video_service import VideoService
from src.tests.utils import BaseTestCase


class APITestCase(BaseTestCase):
    def test_ping_ok(self):
        """test health edpoint returns 200 when available
        """
        response = self.simulate_get("/v1/ping")
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"pong": "OK"})

    def test_videos_empty(self):
        """test count is 0 and data is empty list when no data
        """
        response = self.simulate_get("/v1/videos")
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"count": 0, "data": []})

    def test_videos_not_empty(self):
        """test count is 0 and data is empty list when no data
        """
        v = {
            "state": "California",
            "city": "San Diego",
            "edit_at": "meh",
            "date": "2020-06-01",
            "date_text": "June 1st",
            "pbid": "ca-sandiego-1",
        }
        video = VideoService.create_video(**v)
        LinkService.create_link(
            video,
            "http://shitpissfuckcuntcocksuckermotherfuckertitsfartterdandtwat.com",
        )
        response = self.simulate_get("/v1/videos")
        self.assertEqual(response.status, falcon.HTTP_OK)
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
                        "city": "San Diego",
                        "links": [
                            {
                                "key": None,
                                "link": "http://shitpissfuckcuntcocksuckermotherfuckertitsfartterdandtwat.com",  # noqa
                                "spaces_url": "",
                            }
                        ],
                    }
                ],
            },
        )
