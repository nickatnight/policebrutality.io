from typing import List

from app.models.link import Link
from app.models.video import Video
from app.utils.s3 import download_video, upload_to_spaces


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
        existing_links = [l.link for l in Link.objects()]  # noqa
        for link_data in links:
            if link_data in existing_links:
                continue

            file_name = download_video(link_data)
            link_obj = Link(video=video, link=link_data)

            if file_name:
                upload_to_spaces(file_name)
                link_obj.key = file_name

            link_obj.save()
