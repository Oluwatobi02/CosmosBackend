from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app import socketio
from flask_socketio import join_room, leave_room, emit
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.message_service import MessageService
from app.models.message import Msg, SingleMessage, GroupMessage, Message

msg_bp = Blueprint('messages', __name__)

@msg_bp.route('/recents')
@jwt_required()
def recent_msg():
    user_id = get_jwt_identity()
    recents = MessageService.get_recent_message_list(user_id)
    return jsonify(single=recents[0], group=recents[1])


@msg_bp.route('/<msg>')
@jwt_required()
def get_messages(msg):
    messages = MessageService.get_messages(msg)
    return jsonify(messages)

@msg_bp.route('/', methods=['POST'])
@jwt_required()
def create_chat():
    user_id = get_jwt_identity()
    data = request.get_json()
    result = MessageService.create_message(data)
    return jsonify(success=result)

@socketio.on('single-chat-room')
def send_message(data):
    room = data['messageid']
    msg = Msg(
        sender= data['sender'],
        message= data['message'],
        time= str(datetime.now(timezone.utc))
            ) 
      
    if data['message_type'] == 'single':
        emit('single-chat', msg.to_dict(), to=room)
        message = SingleMessage.objects(id=room).first()
        message.addMessage(msg)
        message.save()
    else:
        message = GroupMessage.objects(id=room).first()
        message.addMessage(msg)
        message.save()

@socketio.on('join-single-chat')
def join_single_chat(data):
    room = data.get('room')
    join_room(room)
    emit('events',f'{data.get("name")} has joined the chat',to=room)

@socketio.on('testing')
def testing(data):
    room = data['room']
    msg = data['message']
    emit('events', msg + "omg", to=data['room'])