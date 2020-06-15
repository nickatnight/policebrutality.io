import importlib
import os

from mongoengine import Document, StringField, ReferenceField

from src.models.video import Video


settings = importlib.import_module("src.settings.{}".format(os.getenv("ENV", "dev")))


class Link(Document):
    video = ReferenceField(Video)
    link = StringField(max_length=255, required=True, unique=False)
    key = StringField(max_length=255, required=False, unique=False)

    def get_url(self):
        return f"{settings.SPACES_URL}{self.key}" if self.key else ""
