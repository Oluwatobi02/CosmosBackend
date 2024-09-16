from datetime import datetime
from app.models.organizer import Organizer
from app.models.event import Event, Onboarding
from app.models.speaker import Speaker
from app.utils.helper import get_hex_hash
from bson import ObjectId
from collections import defaultdict
class EventService:
    @staticmethod
    def createEvent(event_info):
        try:
            fevent, org_speak, onboard = EventService.format_event_to_create(event_info)
            event = Event(
                **fevent
            )
            if onboard:
                onBoarding = Onboarding(**onboard)
                event.onboarding = onBoarding
            
            event.save()
            if fevent.get('picture'):
                event.add_picture(fevent.get('picture'))
            for speaker_id in org_speak['speakers']:
                speaker = Speaker.objects(id=speaker_id).first()
                if not speaker:
                    speaker = Speaker(
                        id=ObjectId(speaker_id)
                    )
                    speaker.save()
                speaker.add_event(event.id)
                speaker.save()
            for organizer in org_speak['organizers']:
                host = Organizer.objects(id=organizer).first()
                if not host:
                    host = Organizer(
                        id=ObjectId(organizer)
                    )
                    host.save()
                host.add_event(event.id)
                host.save()
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def format_event_to_create(event_info):
        event_ = {
            'title': event_info.get('title'),
            'description': event_info.get('description'),
            'picture': event_info.get('picture'),
            'start_date': event_info.get('start_date'),
            'end_date' : event_info.get('end_date'),
            'location': event_info.get('location'),
            'eventtype': event_info.get('eventtype'),
            'no_of_guest': event_info.get('no_of_guest'),
            'created_at': event_info.get('created_at'),
            'organizers': event_info.get('organizers'),
            'speakers': event_info.get('speakers')
        }
        org_speak = {
            'organizers': event_info.get('organizers'),
            'speakers': event_info.get('speakers')
            }
        onboarding = event_info.get('onboarding')
        return event_, org_speak, onboarding
    
    @staticmethod
    def get_event(user_id, event_id):
        event = Event.objects(id=event_id).first()
        return event
    
    @staticmethod
    def get_events_for_message(user_id):
        try:
            organizer = Organizer.objects(id=user_id).first()
            speaker = Speaker.objects(id=user_id).first()
            event_team = []
            oevent = {}
            sevent = {}
            if organizer:
                for event in organizer.events:
                    members = event.organizers + event.speakers

                    oevent = event.team_dict()
                    oevent['members'] = []
                    for member in members:
                        member = member.team_dict()
                        if member['id'] == user_id:
                            continue
                        member['memberid'] = get_hex_hash([user_id, member['id']])
                        oevent['members'].append(member)
                    event_team.append(oevent)
            if speaker:
                for event in speaker.events:
                    sevent = event.team_dict()
                    members = event.speakers + event.organizers
                    sevent['members'] = []
                    for member in members:
                        member = member.team_dict()
                        if member['id'] == user_id:
                            continue
                        member['memberid'] = get_hex_hash([user_id, member['id']])
                        sevent['members'].append(member)
                    event_team.append(sevent)                       
            return event_team
        except Exception as e:
            return f'{e}'