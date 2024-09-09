from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def generate_token(user):
    expires = timedelta(days=1)
    return create_access_token(identity=str(user.id), expires_delta=expires)