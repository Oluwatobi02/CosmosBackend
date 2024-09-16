from app.models.organizer import Organizer
from app.models.speaker import Speaker
from app.models.user import User
from app.models.message import SingleMessage, GroupMessage, Message
from app.utils.helper import gen_random_byte_hex, get_hex_hash
from bson import ObjectId

class MessageService:
    @staticmethod
    def get_recent_message_list(user_id):
        single_message_list = []
        group_message_list = []
        organizer = Organizer.objects(id=user_id).first()
        speaker = Speaker.objects(id=user_id).first()
        if organizer:
            for msg in organizer.singles:
                msg = SingleMessage.objects(id=msg.id).first()
                single_message_list.append(msg.preview())
            for msg in organizer.groups:
                msg = GroupMessage.objects(id=msg.id).first()
                group_message_list.append(msg.preview())
        if speaker:
            for msg in speaker.singles:
                msg = SingleMessage.objects(id=msg.id).first()
                single_message_list.append(msg.preview())
            for msg in speaker.groups:
                msg = GroupMessage.objects(id=msg.id).first()
                group_message_list.append(msg)
        return [single_message_list, group_message_list]
    
    @staticmethod
    def create_message(data):
        try:
            message_type = data.get('message_type')
            
            if message_type == 'single':
                message = SingleMessage.objects(id=get_hex_hash(data.get('members')))
                if message:
                    return True
                message = SingleMessage(
                    id=ObjectId(get_hex_hash(data.get('members'))),
                    message_type=message_type,
                    members=data.get('members'),
                    event=[data.get('event')]
                )
                message.save()

                for member in data.get('members'):
                    organizer = Organizer.objects(id=member).first()
                    speaker = Speaker.objects(id=member).first()
                    
                    if organizer:
                        organizer.add_single(message.id)
                        organizer.save()
                    if speaker:
                        speaker.add_single(message.id)
                        speaker.save()

            else:
                message = GroupMessage( 
                    id=ObjectId(gen_random_byte_hex()),
                    message_type=data.get('message_type'),
                    members=data.get('members'),
                    event=[data.get('event')],
                    name=data.get('name'),
                    organizer=data.get('organizer')
                )
                message.save()

                for member in message.members:
                    organizer = Organizer.objects(id=member.id).first()
                    speaker = Speaker.objects(id=member.id).first()
                    
                    if organizer:
                        organizer.add_group(message.id)
                        organizer.save()
                    if speaker:
                        speaker.add_group(message.id)
                        speaker.save()
            message.save()
            return True
        except Exception as e:
            return f'{e}'