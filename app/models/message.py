from flask_mongoengine import MongoEngine
db = MongoEngine()

class Msg(db.EmbeddedDocument):
    sender = db.ReferenceField('User')
    message = db.StringField()
    time = db.DateTimeField()

    def to_dict(self):
        return {
            'sender': {
                'id': self.sender['id'],
                'name': self.sender['name'],
                'picture': self.sender['basic_info']['picture'],
            },
            'message' : self.message,
            'time': self.time
        }
class Message(db.Document):
    meta = {
        'allow_inheritance': True
    }
    id = db.StringField(primary_key=True)
    messages :list[Msg] = db.ListField(db.EmbeddedDocumentField(Msg))
    message_type = db.StringField()
    people = db.ListField(db.ReferenceField('User'))
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

    def addMessage(self, message : Msg):
        self.messages.append(message)
    
    def to_dict(self):
        return {
            'messages':  [msg.to_dict() for msg in self.messages],
            'message_type': self.message_type,
            'people': self.getPeopleInfo(),
            'event': self.event['title']
        }
    def preview(self):
        return {
            'id': str(self.id),
            'last_message': self.messages[-1],       
        }

class SingleMessage(Message):
    pass

class GroupMessage(Message):
    name = db.StringField()
    picture = db.StringField()
    organizer = db.ReferenceField('Organizer')


    def preview(self):

        return {
            'id': str(self.id),
            'last_message': self.messages[-1],
            'picture': self.picture
        }
