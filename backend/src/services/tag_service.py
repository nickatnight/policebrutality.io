from typing import List

from src.models.tag import Tag
from src.models.video import Video


class TagService(object):
    """service for Tag objects
    """

    @classmethod
    def create_tag(cls, name: str) -> Tag:
        """create Tag instance
        :param name:                name of tag
        :return:                    Tag instance
        """
        tag = Tag(name=name.lower()).save()
        return tag

    @classmethod
    def get_or_create(cls, name: str) -> Tag:
        """get or create Tag instance
        :param name:                name of tag
        :return:                    Tag instance
        """
        tags = Tag.objects(name__iexact=name)
        if tags:
            return tags[0]
        return cls.create_tag(name)

    @classmethod
    def get_tags_from_list(cls, tag_list: List[str]) -> List[Tag]:
        """fetch list of Tag instances by list of strings
        :param tag_list:            list of tag names
        :return:                    list of Tag instance
        """
        tag_instances = list()

        for tag in tag_list:
            tag_instances.append(cls.get_or_create(tag))

        return tag_instances

    @staticmethod
    def create_response_list(video: Video) -> List[str]:
        """create list of Tag.name
        :param video:               Video to grab Tags from
        :return:                    list of Tags as str
        """
        return [tag.name for tag in video.tags]
