from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = MongoEngine()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")