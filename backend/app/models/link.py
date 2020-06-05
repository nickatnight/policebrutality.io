from mongoengine import Document, StringField, ReferenceField

from app.models.video import Video


class Link(Document):
    video = ReferenceField(Video)
    link = StringField(max_length=255, required=True, unique=False)
    key = StringField(max_length=255, required=False, unique=False)
