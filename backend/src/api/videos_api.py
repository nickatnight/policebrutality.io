import falcon

from src.models.video import Video
from src.services.link_service import LinkService
from src.utils.helpers import format_json_response


class VideosAPI(object):
    def on_get(self, req: falcon.Request, resp: falcon.Request) -> falcon.Request:
        """get list of Video objects

        :param req:
        :param resp:
        :return:                formatted response
        """
        resp.status = falcon.HTTP_200
        videos = []

        for video in Video.objects():
            videos.append(
                {
                    "id": video.pbid,
                    "edit_at": video.edit_at,
                    "date": video.date,
                    "date_text": video.date_text,
                    "name": video.name,
                    "state": video.state,
                    "city": video.city,
                    "links": LinkService.create_response_list(video),
                }
            )

        resp.status = falcon.HTTP_200
        resp.media = format_json_response(videos)
