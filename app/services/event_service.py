from datetime import datetime
from app.models.organizer import Organizer
from app.models.event import Event, Onboarding
from app.models.speaker import Speaker
from bson import ObjectId
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
                event.save()
            for organizer in org_speak['organizers']:
                host = Organizer.objects(id=organizer).first()
                if not host:
                    host = Organizer(
                        id=ObjectId(organizer)
                    )
                host.add_event(event.id)
                host.save()
            for speaker_id in org_speak['speakers']:
                speaker = Speaker.objects(id=speaker_id).first()
                if not speaker:
                    speaker = Speaker(
                        id=ObjectId(speaker_id)
                    )
                speaker.add_event(event.id)
                speaker.save()
            return True
        except:
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