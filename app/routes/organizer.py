from flask import Blueprint, request, jsonify
from app.models.organizer import Organizer
organizer_bp = Blueprint('organizer', __name__)



@organizer_bp.route('/<org_id>')
def get_organizer(org_id):
    organizer = Organizer.objects(id=org_id).first()
    return jsonify(organizer.to_dict())