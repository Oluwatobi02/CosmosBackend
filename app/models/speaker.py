from flask_mongoengine import MongoEngine
from datetime import datetime
from app.models.user import User
from app.models.message import SingleMessage, GroupMessage

db = MongoEngine()
class Speaker(db.Document):
    id = db.ObjectIdField(primary_key=True, required=True)
    events = db.ListField(db.ReferenceField('Event'))
    singles = db.ListField(db.ReferenceField('SingleMessage'))
    groups = db.ListField(db.ReferenceField('GroupMessage'))

    def to_dict(self):
        user = User.objects(id=self.id).first()
        res = {
            **user.to_dict(),
        }
        return res
    def add_single(self, messageId):
        self.singles.append(messageId)

    def add_group(self, messageId):
        self.groups.append(messageId)

    def add_event(self, event_id):
        self.events.append(event_id)
        user = User.objects(id=self.id).first()
        user.add_notification("You have been added as a speaker to an event", "Event")
        self.save()

    def get_events(self):
        from app.models.event import Event
        events = []
        for event in self.events:
            event_acc = Event.objects(id=event.id).first()
            events.append(event_acc.to_dict())
        return events

    def team_dict(self):
        user = User.objects(id=str(self.id)).first()
        res = {**user.to_base_dict()}
        return res