from typing import List, Dict

from src.models.link import Link
from src.models.video import Video
from src.services.link_service import LinkService
from src.services.tag_service import TagService
from src.utils.s3 import tmp_folder_clean_up


class VideoService(object):
    """Service for creating a new Video objects
    """

    @classmethod
    def generate_api_response(cls) -> List[Dict]:
        """generate list of Video data for api
        :return:                list of Video data
        """
        videos = list()

        for v in cls.list_videos():
            videos.append(
                {
                    "id": v.pbid,
                    "edit_at": v.edit_at,
                    "date": v.date,
                    "date_text": v.date_text,
                    "name": v.name,
                    "state": v.state,
                    "city": v.city,
                    "description": v.description,
                    "tags": TagService.create_response_list(v),
                    "links": LinkService.create_response_list(v),
                }
            )

        return videos

    @classmethod
    def list_videos(cls) -> List[Video]:
        """Get Video
        :return:
        """
        return Video.objects()

    @staticmethod
    def create_video(**kwargs: int) -> Video:
        """Create a new video
        """
        tags_from_data = kwargs.pop("tags", [])
        tags = TagService.get_tags_from_list(tags_from_data)
        video = Video(tags=tags, **kwargs).save()
        return video

    @staticmethod
    def get_video(pbid: str) -> Video:
        """Get video by link
        :param link:
        """
        return Video.objects(pbid=pbid).first()

    @staticmethod
    def update_video(pbid: str, data: Dict) -> None:
        """
        :param pbid:                id of instance from 2020policebrutality repo
        :param data:                instance data
        :return:                    nothing
        """
        video = Video.objects.get(pbid=pbid)
        incoming_links = data.pop("links", [])
        incoming_tags = data.pop("tags", [])
        tags = TagService.get_tags_from_list(incoming_tags)

        video.modify(tags=tags, **data)
        existing_video_links = [l.link for l in Link.objects(video=video)]  # noqa

        for link in incoming_links:
            if link.get("url") in existing_video_links:
                LinkService.update_link_key(link)
            else:
                LinkService.create_link(video, link)

            tmp_folder_clean_up()
