# app/routes/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.models.user import User
from werkzeug.security import generate_password_hash
print('pass3:', generate_password_hash('123456'))

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # print('[DEBUG] received data:', data)
    # print('[DEBUG] username =', data.get('user_name'))
    # print('[DEBUG] password =', data.get('user_password'))
    user = User.query.filter_by(user_name=data['user_name']).first()
    if user and check_password_hash(user.user_password, data['user_password']):
        return jsonify({'code': 0, 'message': '登录成功', 'user': user.to_dict()})
    return jsonify({'code': 1, 'message': '用户名或密码错误'}), 401
