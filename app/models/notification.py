import uuid
from flask_mongoengine import MongoEngine
db = MongoEngine()
from app.utils.helper import Helper

class Notification(db.EmbeddedDocument):
    meta = {
    'allow_inheritance': True
            }
    id = db.StringField(default=str(uuid.uuid4()), required=True, unique=True)
    message = db.StringField(required=True)
    tag = db.StringField(required=True)
    created_at = db.DateTimeField(required=True)

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "tag": self.tag,
            "created_at": Helper.convert_to_readable(self.created_at)
        }


class MessageNotification(Notification):
    link = db.StringField()
    sender_name = db.StringField()
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "tag": self.tag,
            "link": self.link,
            "sender_name": self.sender_name,
            "created_at": Helper.convert_to_readable(self.created_at)
        }

class EventNotification(Notification):
    link = db.StringField()
    organizer_name = db.StringField()
    organizer_email = db.StringField()
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "tag": self.tag,
            "link": self.link,
            "organizer_name": self.organizer_name,
            "organizer_email": self.organizer_email,
            "created_at": Helper.convert_to_readable(self.created_at)
        }    

class UpcomingEventNotification(Notification):
    event_name = db.StringField()
    event_date = db.DateTimeField()
    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "tag": self.tag,
            "event_name": self.event_name,
            "event_date": Helper.convert_to_readable(self.event_date),
            "created_at": Helper.convert_to_readable(self.created_at)
        }
