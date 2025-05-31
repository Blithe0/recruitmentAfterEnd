from flask import Blueprint, jsonify, request
from marshmallow import EXCLUDE
from app.extensions import db
from app.models.interviewer import Interviewer
from app.schemas.interviewer import InterviewerSchema

interviewer_bp = Blueprint('interviewer', __name__, url_prefix='/api/interviewer')
schema = InterviewerSchema()
schemas = InterviewerSchema(many=True)

# 获取所有面试官
# @interviewer_bp.route('/list', methods=['GET'])
@interviewer_bp.route('/', methods=['GET'])
def get_all():
    data = Interviewer.query.all()
    return jsonify({'code': 0, 'data': schemas.dump(data)})

# 获取下拉选项
@interviewer_bp.route('/options', methods=['GET'])
def get_options():
    data = Interviewer.query.all()
    options = [{'label': i.name, 'value': i.interviewer_id} for i in data]
    return jsonify({'code': 0, 'data': options})

# 新增
@interviewer_bp.route('/add', methods=['POST'])
def add():
    data = schema.load(request.json)
    interviewer = Interviewer(**data)
    db.session.add(interviewer)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '添加成功', 'data': schema.dump(interviewer)})

# 更新
@interviewer_bp.route('/update/<int:id>', methods=['PUT'])
def update(id):
    interviewer = Interviewer.query.get(id)
    if not interviewer:
        return jsonify({'code': 1, 'msg': '面试官不存在'}), 404

    try:
        # data = schema.load(request.json)
        data = schema.load(request.json, unknown=EXCLUDE)  # 关键修改
        interviewer.name = data['name']
        interviewer.department_id = data['department_id']
        interviewer.contact = data.get('contact', '')
        db.session.commit()
        return jsonify({'code': 0, 'msg': '更新成功'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '服务器错误', 'error': str(e)}), 500

# 删除
@interviewer_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    interviewer = Interviewer.query.get(id)
    if not interviewer:
        return jsonify({'code': 1, 'msg': '面试官不存在'}), 404

    db.session.delete(interviewer)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '删除成功'})
