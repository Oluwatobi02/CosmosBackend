from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
msg_bp = Blueprint('messages', __name__)

@msg_bp.route('/recents')
@jwt_required()
def recent_msg():
    pass