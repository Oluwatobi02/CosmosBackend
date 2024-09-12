from flask import Blueprint, request, jsonify
from app import socketio
from flask_socketio import join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.message_service import MessageService
from app.models.message import Msg, SingleMessage, GroupMessage
msg_bp = Blueprint('messages', __name__)

@msg_bp.route('/recents')
@jwt_required()
def recent_msg():
    user_id = get_jwt_identity()
    recents = MessageService.get_recent_message_list(user_id)
    return jsonify(single=recents[0], group=recents[1])


@msg_bp.route('/join_room')
def handle_join_room():
    room = request.get_json()['room']
    join_room(room)
    return jsonify(success=True)

@msg_bp.route('/leave_room')
def handle_leave_room():
    room = request.get_json()['room']
    leave_room(room)
    return jsonify(success=True)
    
@socketio.on('message')
@jwt_required()
def send_message(data):
    user_id = get_jwt_identity()
    room = data['messageid']
    msg = Msg(
        sender= data['sender'],
        message= data['message'],
        time= data['time']
            )   
    socketio.emit('message', msg.to_dict(), to=room)
    if data['message_type'] == 'single':
        message = SingleMessage(id=data['id'])
        message.addMessage(msg)
    else:
        message = GroupMessage(id-data['id'])
        message.addMessage(msg)
    """
    {
        "sender": id,
        "message": body of the message,
        "time" : time of the message,
        "messageid": id of the message,
    }

    return {
            "sender": {
                        id: sender id,
                        picture: sender picture,
                        name: sender name
                    }
            "message": body of the message,
            "time": time of the message,
            
        }
    """



@msg_bp.route('/test')
def testing():
    return jsonify(success=True)