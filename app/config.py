import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mouse')
    REDIS_CONFIG = {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': 6379,
        'decode_responses': True,
    }
    MONGODB_SETTINGS = {
        'db': 'test',
        'host': os.getenv('MONGODB_URI', ''),
        'port': 27017,
    }
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')