from flask_mongoengine import MongoEngine
db = MongoEngine()


class Msg(db.EmbeddedDocument):
    sender = db.ReferenceField('User')
    message = db.StringField()
    time = db.DateTimeField()

    def to_dict(self):
        return {
            'sender': self.sender,
            'message' : self.message,
            'time': self.time
        }


class Message(db.Document):
    meta = {
        'allow_inheritance': True
    }
    id = db.StringField(primary_key=True)
    messages = db.ListField(db.EmbeddedDocumentField(Msg))
    message_type = db.StringField()
    people = db.ListField(db.GenericReferenceField())
    event = db.ListField(db.ReferenceField('Event'))

    def getPeopleInfo(self):
        info = {}
        for person in self.people:
            info[str(person.id)] = {
                'name': person['name'],
                'picture': person['picture'],
                'title': person['title']
            }
        return info

    def addMessage(self, message):
        msg = Msg(sender=message['sender'], message=message['message'], time=message['time'])
        self.messages.append(msg)
    
    def to_dict(self):
        return {
            'messages':  [msg.to_dict() for msg in self.messages],
            'message_type': self.message_type,
            'people': self.getPeopleInfo(),
            'event': self.event['title']
        }


class SingleMessage(Message):
    pass

class GroupMessage(Message):
    name = db.StringField()
    organizer = db.ReferenceField('Organizer')