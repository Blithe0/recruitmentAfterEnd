from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.selection import Selection
from app.schemas.selection import SelectionSchema
from app.models.plan import Plan

selection_bp = Blueprint('selection', __name__, url_prefix='/api/selection')


@selection_bp.route('/list', methods=['GET'])
def list_selections():
    """
    返回所有选拔流程记录，附带 plan_name。
    """
    selections = Selection.query.all()
    schema = SelectionSchema(many=True)
    return jsonify({'code': 0, 'data': schema.dump(selections)})
    # selections = Selection.query.all()
    # schema = SelectionSchema(many=True)
    # result = []
    # for sel in selections:
    #     # 将单个实例放入 context，以便 post_dump 能取到 plan_name
    #     schema.context = {'obj': sel}
    #     result.append(schema.dump(sel))
    # return jsonify({'code': 0, 'data': result})


@selection_bp.route('/create', methods=['POST'])
def create_selection():
    """
    创建新的选拔流程
    1. 必须包含 'resume_screen'
    2. steps 无重复
    3. plan_id 对应的 Plan 必须存在且 plan_status='approved'
    """
    data = request.json or {}
    plan_id = data.get('plan_id')
    steps = data.get('steps', [])

    # 检查必含简历初筛
    if 'resume_screen' not in steps:
        return jsonify({'code': 1, 'message': '流程中必须包含 “resume_screen” （简历初筛）'}), 400

    # 检查重复
    if len(steps) != len(set(steps)):
        return jsonify({'code': 1, 'message': '流程步骤不能重复'}), 400

    # 检查 plan 是否存在且已通过审核
    plan = Plan.query.get(plan_id)
    if not plan:
        return jsonify({'code': 1, 'message': '对应计划不存在'}), 400
    if plan.plan_status != 'approved':
        return jsonify({'code': 1, 'message': '仅允许对已通过审核的计划设置选拔流程'}), 400

    sel = Selection(
        plan_id=plan_id,
        steps_json=steps
    )
    db.session.add(sel)
    db.session.commit()
    return jsonify({'code': 0, 'message': '创建成功'})


@selection_bp.route('/<int:id>', methods=['PUT'])
def update_selection(id):
    """
    更新已有记录
    同样要保证:
      - 包含 'resume_screen'
      - 无重复
      - 若修改 plan_id，必须对应已通过审核的 Plan
    """
    sel = Selection.query.get(id)
    if not sel:
        return jsonify({'code': 1, 'message': '记录不存在'}), 404

    data = request.json or {}
    steps = data.get('steps', [])
    plan_id = data.get('plan_id')

    if 'resume_screen' not in steps:
        return jsonify({'code': 1, 'message': '流程中必须包含 “resume_screen” （简历初筛）'}), 400
    if len(steps) != len(set(steps)):
        return jsonify({'code': 1, 'message': '流程步骤不能重复'}), 400

    if plan_id:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'code': 1, 'message': '对应计划不存在'}), 400
        if plan.plan_status != 'approved':
            return jsonify({'code': 1, 'message': '仅允许对已通过审核的计划设置选拔流程'}), 400
        sel.plan_id = plan_id

    sel.steps_json = steps
    db.session.commit()
    return jsonify({'code': 0, 'message': '更新成功'})


@selection_bp.route('/<int:id>', methods=['DELETE'])
def delete_selection(id):
    sel = Selection.query.get(id)
    if not sel:
        return jsonify({'code': 1, 'message': '记录不存在'}), 404

    db.session.delete(sel)
    db.session.commit()
    return jsonify({'code': 0, 'message': '删除成功'})
