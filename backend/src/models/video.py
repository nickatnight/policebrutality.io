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

    def generate_string_for_subfolders(self):
        if self.state and self.city:
            sub = f"{self.state}/{self.city}/"
        elif self.state and "unknown" not in self.state.lower():
            sub = f"{self.state}/unknown/"
        else:
            sub = "unknown/"
        return sub.lower()
