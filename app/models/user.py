from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from uuid import uuid4
from app.models.notification import Notification
from app.amazon.upload import upload_file

db = MongoEngine()

class BasicInfo(db.EmbeddedDocument):
    linkedin = db.StringField(default='')
    bio = db.StringField(default='')
    title = db.StringField(default='')
    picture = db.StringField(default='')
    alternative_email = db.StringField(default='')
    website = db.StringField(default='')


class User(db.Document):
    email = db.EmailField(required=True, unique=True)
    password_hash = db.StringField(default='')
    name = db.StringField(required=True)
    basic_info = db.EmbeddedDocumentField(BasicInfo)
    notifications = db.ListField(db.EmbeddedDocumentField(Notification))


    def to_dict(self):
            res = {
                'id': str(self.id),
                'email': self.email,
                'name': self.name,
                'title': self.basic_info.title,
                'linkedin': self.basic_info.linkedin,
                'bio': self.basic_info.bio,
                'picture': self.basic_info.picture,
                'website': self.basic_info.website,
            }
            return res
    
    def test(self):
        print(self.to_dict())
        return [self.name, self.email, self.basic_info.title]


    def add_picture(self, blob_data):
        print('here 2')
        name = str(uuid4())
        print(name)
        link = upload_file(blob_data, name)
        print(link)
        self.basic_info.picture = link
    
    def add_notification(self, message, tag):
        notification = Notification(message=message, tag=tag, created_at=datetime.now())
        self.notifications.append(notification)

    def notifications_to_dict(self):
        return [noti.to_dict() for noti in self.notifications]

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
