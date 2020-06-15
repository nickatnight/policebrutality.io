import importlib
import os
from typing import List, Dict

from src.models.link import Link
from src.models.video import Video
from src.utils.s3 import download_video, upload_to_spaces


settings = importlib.import_module("src.settings.{}".format(os.getenv("ENV", "dev")))


class LinkService(object):
    """Service for creating a new Link objects
    """

    # TODO: add collections update

    @classmethod
    def process_video(cls, link: str) -> str:
        file_name = download_video(link)
        empty_key = ""

        if file_name:
            # save videos to filesystem for local dev
            if not settings.IS_DEV:
                upload_to_spaces(file_name)

        return file_name or empty_key

    @classmethod
    def update_link_key(cls, link: str) -> None:
        """udpdate Link.key if missing

        :param video:
        :param link:
        :return:            nothing
        """
        link_obj = Link.objects.get(link=link)

        # TODO: add check for supported sites to avoid wasted calls
        if not link_obj.key:
            key = cls.process_video(link_obj.link)

            if key:
                link_obj.key = key
                link_obj.save()

    @classmethod
    def create_link(cls, video: Video, link: str) -> None:
        link_obj = Link(video=video, link=link)
        key = cls.process_video(link)

        if key:
            link_obj.key = key

        link_obj.save()

    @classmethod
    def create_links(cls, video: Video, links: List[str]) -> None:
        """Create a new Link objects

        :param video:
        :param links:
        :return:
        """
        existing_links = [l.link for l in Link.objects()]  # noqa
        for link_str in links:
            if link_str in existing_links:
                cls.update_link_key(link_str)
                continue
            cls.create_link(video, link_str)

    @staticmethod
    def create_response_list(video: Video) -> List[Dict]:
        """create response data from Link objects

        :param video:
        :return:                list of serialized data
        """
        data = [
            {"key": link.key, "link": link.link, "spaces_url": link.get_url(),}
            for link in Link.objects(video=video)
        ]

        return data
