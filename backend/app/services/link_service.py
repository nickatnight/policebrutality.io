import importlib
import os
from typing import List, Dict

from app.models.link import Link
from app.models.video import Video
from app.utils.s3 import download_video, upload_to_spaces


settings = importlib.import_module("app.settings.{}".format(os.getenv("ENV", "dev")))


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
                if not settings.IS_DEV:
                    upload_to_spaces(file_name)

                # TODO: need volume for local FEE dev
                link_obj.key = file_name

            link_obj.save()

    @staticmethod
    def create_response_list(video: Video) -> List[Dict]:
        """create response data from Link objects

        :param video:
        :return:                list of serialized data
        """
        data = [
            {
                "key": link.key,
                "link": link.link,
                "spaces_url": f"{settings.SPACES_URL}{link.key}" if link.key else "",
            }
            for link in Link.objects(video=video)
        ]

        return data
