import falcon

from src.tests.utils import BaseTestCase



class ResourceTestCase(BaseTestCase):
    def test_ping_ok(self):
        """test health edpoint returns 200 when available
        """
        response = self.simulate_get('/v1/ping')
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"pong": "OK"})

    def test_videos_empty(self):
        """test count is 0 and data is empty list when no data
        """
        response = self.simulate_get('/v1/videos')
        self.assertEqual(response.status, falcon.HTTP_OK)
        self.assertEqual(response.json, {"count": 0, "data": []})
