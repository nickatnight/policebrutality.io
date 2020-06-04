from typing import List

from app.models.video import Video


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
