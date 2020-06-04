import falcon

from app.models.video import Video
from app.utils.helpers import format_json_response


class VideoResource(object):
    def on_get(self, req: falcon.Request, resp: falcon.Request) -> falcon.Request:
        resp.status = falcon.HTTP_200
        videos = []

        for video in Video.objects():
            videos.append(
                {
                    "city": video.city,
                    "link": video.link,
                    "state": video.state,
                    "title": video.title,
                }
            )
        resp.status = falcon.HTTP_200
        resp.media = format_json_response(videos)
