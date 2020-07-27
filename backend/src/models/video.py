from mongoengine import Document, StringField, ListField, ReferenceField

from src.models.tag import Tag


class Video(Document):
    pbid = StringField(max_length=255, required=True)
    edit_at = StringField(max_length=255, required=False)
    date = StringField(max_length=255, required=False)
    date_text = StringField(max_length=255, required=False)
    name = StringField(max_length=255, required=False)
    state = StringField(max_length=200, required=False)
    city = StringField(max_length=200, required=False)
    description = StringField(required=False)
    tags = ListField(ReferenceField(Tag))
