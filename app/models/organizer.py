from flask_mongoengine import MongoEngine
from datetime import datetime
from app.models.user import User
from app.models.message import GroupMessage, SingleMessage, Msg

db = MongoEngine()

class Organizer(db.Document):
    id = db.ObjectIdField(primary_key=True, required=True)
    events = db.ListField(db.ReferenceField('Event'))
    singles = db.ListField(db.ReferenceField('singlemessage'))
    groups = db.ListField(db.ReferenceField('groupmessage'))

    def add_event(self, event_id):
        self.events.append(event_id)
        user = User.objects(id=self.id).first()
        user.add_notification("Your Event has been created", "Event")

    def get_events(self):
        return [
            event.to_dict() for event in self.events
        ]

    def to_dict(self):
        user = User.objects(id=self.id).first()
        res = {
            **user.to_dict(),

        }
        return res
    
