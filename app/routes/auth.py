from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/token', methods=['POST'])
def authenticate():
    data = request.get_json()
    email, password = data['email'], data['password']
    token = AuthService.authenticate_user(email, password)
    if token:
        return jsonify(success=True, token=token)
    else:
        return jsonify(success=False)
    
@auth_bp.route('/register', methods=['POST'])
def register_user():
    user_info = request.get_json()
    result = AuthService.create_user(user_info)
    return jsonify(success=result)

@auth_bp.route('/test', methods=['POST'])
def test_route():
    data = request.get_json()
    print(data, 'here')
    return jsonify(data=data)

@auth_bp.route('/test')
def testing():
    print('hit')
    return jsonify(message='successful')