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
    def process_video(cls, link_obj: Link) -> str:
        """download/process video
        :param link:                url to video (or lack thereof)
        :return:                    unique key for video
        """
        file_name = download_video(link_obj.link)
        empty_key = ""

        if file_name:
            key = link_obj.video.generate_string_for_subfolders()
            # save videos to filesystem for local dev
            if not settings.IS_DEV:
                upload_to_spaces(key, file_name)

            file_name = key + file_name

        return file_name or empty_key

    @classmethod
    def update_link_key(cls, link: Dict) -> None:
        """update Link.key if missing

        :param video:
        :param link:
        :return:            nothing
        """
        link_obj = Link.objects(link=link.get("url")).first()

        # TODO: add check for supported sites to avoid wasted calls
        if not link_obj.key:
            key = cls.process_video(link_obj)

            if key:
                link_obj.key = key
                link_obj.save()

    @classmethod
    def create_link(cls, video: Video, link_data: Dict) -> None:
        """creat Link instance
        :param video:               Video instance
        :param link_data:           "link" data from all-locations-v2.json instance
        :return:                    nothing
        """
        link_obj = Link(
            video=video,
            link=link_data.get("url"),
            text=link_data.get("text", None) or None,
        )
        key = cls.process_video(link_obj)

        if key:
            link_obj.key = key

        link_obj.save()

    @classmethod
    def create_links(cls, video: Video, links: List[Dict]) -> None:
        """Create a new Link objects

        :param video:
        :param links:
        :return:
        """
        existing_links = [l.link for l in Link.objects()]  # noqa
        for link_data in links:
            link_url = link_data.get("url", None) or None
            if link_url:
                if link_url in existing_links:
                    cls.update_link_key(link_data)
                    continue
                cls.create_link(video, link_data)

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
                "text": link.text,
                "spaces_url": link.get_url(),
            }
            for link in Link.objects(video=video)
        ]

        return data

    @staticmethod
    def list_links() -> List[Link]:
        """
        :return:            list of Links
        """
        return Link.objects()
