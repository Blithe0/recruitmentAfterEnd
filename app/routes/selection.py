from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.selection import Selection
from app.schemas.selection import SelectionSchema

selection_bp = Blueprint('selection', __name__, url_prefix='/api/selection')


@selection_bp.route('/list', methods=['GET'])
def list_selections():
    selections = Selection.query.all()
    schema = SelectionSchema(many=True)
    return jsonify({'code': 0, 'data': schema.dump(selections)})


@selection_bp.route('/create', methods=['POST'])
def create_selection():
    data = request.json
    schema = SelectionSchema()
    selection = schema.load(data)
    db.session.add(selection)
    db.session.commit()
    return jsonify({'code': 0, 'message': '创建成功'})


@selection_bp.route('/<int:id>', methods=['PUT'])
def update_selection(id):
    selection = Selection.query.get(id)
    if not selection:
        return jsonify({'code': 1, 'message': '记录不存在'}), 404
    data = request.json
    for key, value in data.items():
        setattr(selection, key, value)
    db.session.commit()
    return jsonify({'code': 0, 'message': '更新成功'})


@selection_bp.route('/<int:id>', methods=['DELETE'])
def delete_selection(id):
    selection = Selection.query.get(id)
    if not selection:
        return jsonify({'code': 1, 'message': '记录不存在'}), 404
    db.session.delete(selection)
    db.session.commit()
    return jsonify({'code': 0, 'message': '删除成功'})
