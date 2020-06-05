from mongoengine import Document, StringField, ReferenceField

from app.models.video import Video


class Link(Document):
    video = ReferenceField(Video)
    link = StringField(max_length=255, required=True, unique=True)
