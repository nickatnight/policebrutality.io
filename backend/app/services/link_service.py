from typing import List

from app.models.link import Link
from app.models.video import Video


class LinkService(object):
    """Service for creating a new Link objects
    """

    @staticmethod
    def create_links(video: Video, links: List[str]) -> None:
        """Create a new video

        :param video:
        :param links:
        :return:
        """
        for link_data in links:
            Link(video=video, link=link_data).save()
