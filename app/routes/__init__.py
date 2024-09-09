from .organizer import organizer_bp
from .speaker import speaker_bp
from .auth import auth_bp
from .event import event_bp
from .user import user_bp
from.message import msg_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(speaker_bp, url_prefix='/speakers')
    app.register_blueprint(msg_bp, url_prefix='/messages')
    app.register_blueprint(organizer_bp, url_prefix='/organizer')
    app.register_blueprint(event_bp, url_prefix='/events')