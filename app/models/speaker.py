from flask_mongoengine import MongoEngine
from datetime import datetime
from app.models.user import User
from app.models.message import SingleMessage, GroupMessage

db = MongoEngine()


class Speaker(db.Document):
    id = db.ObjectIdField(primary_key=True, required=True)
    events = db.ListField(db.ReferenceField('Event'))
    singles = db.ListField(db.ReferenceField('singlemessage'))
    groups = db.ListField(db.ReferenceField('groupmessage'))


    def to_dict(self):
        user = User.objects(id=self.id).first()
        res = {
            **user.to_dict(),
        }
        return res
    

    def add_event(self, event_id):
        self.events.append(event_id)
        user = User.objects(id=self.id).first()
        user.add_notification("You have been added as a speaker to an event", "Event")

    def get_events(self):
        return [event.to_dict() for event in self.events]