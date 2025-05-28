# app/routes/user.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.extensions import db

# user_bp = Blueprint('user', __name__, url_prefix='/user')
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@user_bp.route('', methods=['POST'])
def add_user():
    data = request.get_json()
    if not all(k in data for k in ('user_name', 'user_password', 'user_role')):
        return jsonify({'error': 'Missing fields'}), 400
    user = User(
        user_name=data['user_name'],
        user_password=generate_password_hash(data['user_password']),
        user_role=data['user_role'],
        user_phone=data.get('user_phone', ''),
        user_card=data.get('user_card', ''),
        user_sex=data.get('user_sex', '')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User added'})

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.user_name = data.get('user_name', user.user_name)
    if 'user_password' in data:
        user.user_password = generate_password_hash(data['user_password'])
    user.user_role = data.get('user_role', user.user_role)
    user.user_phone = data.get('user_phone', user.user_phone)
    user.user_card = data.get('user_card', user.user_card)
    user.user_sex = data.get('user_sex', user.user_sex)
    db.session.commit()
    return jsonify({'message': 'User updated'})

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})
