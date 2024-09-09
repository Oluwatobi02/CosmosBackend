from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt,socketio
from .routes import register_routes
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    
    
    

    register_routes(app)

    return app
