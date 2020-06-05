import falcon

from app.models.link import Link
from app.models.video import Video
from app.utils.helpers import format_json_response


class VideoResource(object):
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
                    "edit_at": video.edit_at,
                    "date": video.date,
                    "date_text": video.date_text,
                    "name": video.name,
                    "state": video.state,
                    "city": video.city,
                    "links": [link.link for link in Link.objects(video=video)],
                }
            )
        resp.status = falcon.HTTP_200
        resp.media = format_json_response(videos)
