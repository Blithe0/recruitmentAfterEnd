# app/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(user_name=data['user_name']).first()
    if user and check_password_hash(user.user_password, data['user_password']):
        return jsonify({'message': 'Login successful', 'user': user.to_dict()})
    return jsonify({'error': 'Invalid credentials'}), 401
