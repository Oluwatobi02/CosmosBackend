from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.event_service import EventService
from app.services.user_service import UserService
from app.models.organizer import Organizer
from app.models.organizer import Organizer
from app.models.speaker import Speaker
event_bp = Blueprint('events', __name__)


@event_bp.route('/', methods=['POST'])
@jwt_required()
def create_event():
    data = request.get_json()
    data['speakers'] = UserService.get_id_by_emails(data.get('speakers'))
    data['organizers'] = UserService.get_id_by_emails(data.get('organizers'))
    result = EventService.createEvent(data)
    return jsonify(success=result)

@event_bp.route('/<event_id>')
@jwt_required()
def get_event(event_id):
    user_id = get_jwt_identity()
    event = EventService.get_event(user_id, event_id)
    print(event)
    return jsonify(event=event.to_dict())

@event_bp.route('/')
@jwt_required()
def get_user_events():
    user_id = get_jwt_identity()
    organizer = Organizer.objects(id=user_id).first()
    speaker = Speaker.objects(id=user_id).first()
    speaking = speaker.get_events() if speaker else []
    organized = organizer.get_events() if organizer else []
    return jsonify(organized=organized, speaking=speaking)
    
