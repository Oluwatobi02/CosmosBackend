from flask_mongoengine import MongoEngine
from app.amazon.upload import upload_file
db = MongoEngine()
from uuid import uuid4
from app.models.organizer import Organizer
from app.models.speaker import Speaker

class Onboarding(db.DynamicEmbeddedDocument):
    pass

class Event(db.Document):
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    picture = db.StringField()
    start_date = db.DateTimeField(required=True)
    end_date = db.DateTimeField()
    location = db.StringField(required=True)
    eventtype = db.StringField(required=True)
    organizers = db.ListField(db.ReferenceField(Organizer))
    speakers = db.ListField(db.ReferenceField(Speaker))
    no_of_guest = db.IntField(default=0)
    onboarding = db.EmbeddedDocumentField(Onboarding)
    created_at = db.DateTimeField()

    def add_picture(self, blob_data):
        name_ = str(uuid4())
        link = upload_file(blob_data, name_)
        self.picture = link
        self.save()

    def team_dict(self):
        return {
            "id": str(self.id),
            "picture": self.picture,
            "title": self.title
        }
    def to_dict(self):
        speaking = []
        organizing = []
        for speaker in self.speakers:
            print(speaker)
            speaker_acc = Speaker.objects(id=speaker.id).first()
            if speaker:
                speaking.append(speaker_acc.to_dict())
        for organizer in self.organizers:
            print(organizer)
            organizer_acc = Organizer.objects(id=organizer.id).first()
            if organizer:
                organizing.append(organizer_acc.to_dict())
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'picture': self.picture,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'location': self.location,
            'eventtype': self.eventtype,
            'organizers': organizing,
            'speakers': speaking,
            'no_of_guest': self.no_of_guest,
            'created_at': self.created_at
        }
    










    