from mongoengine import Document, StringField


class Tag(Document):
    name = StringField(max_length=255, required=True, unique=False)
