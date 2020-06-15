from typing import List

from src.models.link import Link
from src.models.video import Video
from src.services.link_service import LinkService
from src.utils.s3 import tmp_folder_clean_up


class VideoService(object):
    """Service for creating a new Video objects
    """

    @staticmethod
    def create_video(**kwargs: int) -> Video:
        """Create a new video
        """
        video = Video(**kwargs).save()
        return video

    @staticmethod
    def list_videos() -> List[Video]:
        """Get created projects
        :return:
        """
        return Video.objects()

    @staticmethod
    def delete_video(video_id: int) -> None:
        """Delete the video
        :param video_id:
        """
        Video.objects(id=video_id).delete()

    @staticmethod
    def get_video(link: str) -> Video:
        """Get video by link
        :param link:
        """
        return Video.objects(link=link)

    @staticmethod
    def update_video(pbid, data):
        video = Video.objects.get(pbid=pbid)
        incoming_links = data.pop("links", [])
        video.modify(**data)
        existing_video_links = [l.link for l in Link.objects(video=video)]  # noqa

        for link in incoming_links:
            if link in existing_video_links:
                LinkService.update_link_key(link)
            else:
                LinkService.create_link(video, link)

            tmp_folder_clean_up()
