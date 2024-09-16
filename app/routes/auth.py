from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required
from app import socketio
from flask_socketio import emit, join_room, leave_room
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/token', methods=['POST'])
def authenticate():
    data = request.get_json()
    email, password = data['email'], data['password']
    token, userId = AuthService.authenticate_user(email, password)
    if token:
        return jsonify(success=True, token=token, userId=userId)
    else:
        return jsonify(success=False)
    
@auth_bp.route('/register', methods=['POST'])
def register_user():
    user_info = request.get_json()
    result = AuthService.create_user(user_info)
    return jsonify(success=result)

@socketio.on('join-room')
def handle_join_room(data):   
    room = data.get('room')
    if room:
        join_room(room)
        emit('events', f"joined room")

@socketio.on('leave-room')
def handle_leave_room(data):
    room = data.get('room')
    if room:
        leave_room(room)
        emit('events', f'left room f{room}')

@auth_bp.route('/test', methods=['POST'])
def test_route():
    data = request.get_json()
    print(data, 'here')
    return jsonify(data=data)

@auth_bp.route('/test')
def testing():
    print('hit')
    return jsonify(message='successful')
