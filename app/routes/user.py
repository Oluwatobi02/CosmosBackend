from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.search_service import SearchService
from app.utils.algorithms import Trie
from app.amazon.upload import upload_file
from app.redis_config import r, queue


user_bp = Blueprint('users', __name__)

trie = Trie()
emails = set()


@user_bp.route('/search', methods=['POST'])
def search_user():
    global emails
    if len(emails) < 1:
        emails = set(SearchService.populate_emails())
        for email_obj in emails:
            print(email_obj['email'])
            trie.insert(email_obj['email'])
    email = request.get_json()['email']
    res = trie.search(email)

    return jsonify(present=res)