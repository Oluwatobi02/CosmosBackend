from app.models.organizer import Organizer
from app.models.speaker import Speaker
from app.models.user import User
from app.models.message import SingleMessage, GroupMessage
class MessageService:
    @staticmethod
    def get_recent_message_list(user_id):
        single_message_list = set()
        group_message_list = set()
        organizer = Organizer.objects(id=user_id).first()
        speaker = Speaker.objects(id=user_id).first()
        for msg in organizer.singles:
            msg = SingleMessage.objects(id=msg).first()
            single_message_list.add(msg.preview())
        for msg in organizer.groups:
            msg = GroupMessage.objects(id=msg).first()
            group_message_list.add(msg.preview())
        for msg in speaker.singles:
            msg = SingleMessage.objects(id=msg).first()
            single_message_list.add(msg.preview())
        for msg in speaker.groups:
            msg = GroupMessage.objects(id=msg).first()
            group_message_list.add(msg)
        return [single_message_list, group_message_list]
    
    
    
            