from flask import Blueprint, jsonify, request
from app.models.talent import Talent
from app.extensions import db

talent_bp = Blueprint('talent', __name__, url_prefix='/api/talent')

# 获取所有人才
@talent_bp.route('/', methods=['GET'])
def get_all_talent():
    data = Talent.query.all()
    return jsonify([t.to_dict() for t in data])

# 加入内部人才库（由简历触发）
@talent_bp.route('/add_internal', methods=['POST'])
def add_internal_talent():
    data = request.json
    t = Talent(
        talent_name=data.get('name'),
        talent_sex=data.get('gender'),
        talent_type=0,
        talent_phone=data.get('phone', ''),
        talent_card=data.get('card', '')
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '已添加至内部人才库'})

@talent_bp.route('/internal', methods=['GET'])
def get_internal():
    data = Talent.query.filter_by(talent_type=0).all()
    return jsonify([t.to_dict() for t in data])

@talent_bp.route('/external', methods=['GET'])
def get_external():
    result = {
        '技术部': [
            {"talent_name": "张三", "talent_sex": "男", "talent_phone": "123456", "talent_card": "111"},
            {"talent_name": "李四", "talent_sex": "女", "talent_phone": "654321", "talent_card": "222"}
        ],
        '人力资源部': [
            {"talent_name": "王五", "talent_sex": "男", "talent_phone": "333444", "talent_card": "333"}
        ]
    }
    return jsonify(result)

