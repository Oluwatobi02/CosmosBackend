from datetime import timedelta
from flask_jwt_extended import create_access_token

def generate_token(_id):
    expires = timedelta(days=1)
    return create_access_token(identity=_id, expires_delta=expires)