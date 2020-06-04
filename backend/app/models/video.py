from mongoengine import Document, StringField


class Video(Document):
    title = StringField(max_length=200, required=False)
    link = StringField(max_length=255, required=True, unique=True)
    state = StringField(max_length=200, required=False)
    city = StringField(max_length=200, required=False)
