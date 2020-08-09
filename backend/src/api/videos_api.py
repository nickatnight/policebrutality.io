import falcon

from src.services.video_service import VideoService
from src.utils.helpers import format_json_response


class VideosAPI(object):
    def on_get(self, req: falcon.Request, resp: falcon.Request) -> falcon.Request:
        """get list of Video objects

        :param req:
        :param resp:
        :return:                formatted response
        """
        resp.status = falcon.HTTP_200
        videos = VideoService.generate_api_response()
        resp.status = falcon.HTTP_200
        resp.media = format_json_response(videos)
