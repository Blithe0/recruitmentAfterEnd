# routes/plan.py
from flask import Blueprint, request, jsonify
from app.models.plan import Plan
from app.models.demand import Demand
from app.extensions import db
from app.schemas.plan import PlanCreateSchema, PlanResponseSchema
from pydantic import ValidationError
from datetime import datetime

plan_bp = Blueprint('plan', __name__, url_prefix='/api/plan')

# 获取所有招聘计划
@plan_bp.route('/', methods=['GET'])
def get_plan_list():
    plans = Plan.query.join(Demand).all()
    result = []
    for plan in plans:
        result.append({
            "plan_id": plan.plan_id,
            "demand_id": plan.demand_id,
            "user_id": plan.user_id,
            "job_name": plan.job_name,
            "recruit_number": plan.recruit_number,
            "release_time": plan.release_time.isoformat(),
            "use_time": plan.use_time.isoformat(),
            "salary": plan.salary,
            "plan_status": plan.plan_status,

            # 加入关联招聘需求中的字段
            "job_place": plan.demand.job_place,
            "job_description": plan.demand.job_description,
            "job_requirement": plan.demand.job_requirement,
            "reason": plan.demand.reason
        })

    return jsonify(result)
# def get_plan_list():
#     plans = Plan.query.all()
#     return jsonify([plan.to_dict() for plan in plans])


# 创建招聘计划（草稿）
@plan_bp.route('/', methods=['POST'])
def create_plan():
    try:
        schema = PlanCreateSchema(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    plan = Plan(
        demand_id=schema.demand_id,
        user_id=schema.user_id,
        recruit_number=schema.recruit_number,
        release_time=schema.release_time,
        use_time=schema.use_time,
        salary=schema.salary,
        job_name=schema.job_name,
        plan_status='draft'
    )
    db.session.add(plan)
    db.session.commit()
    return jsonify({'message': '招聘计划已创建'}), 201


# 提交草稿计划
@plan_bp.route('/<int:plan_id>/submit', methods=['POST'])
def submit_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    if plan.plan_status not in ['draft', 'rejected']:
        return jsonify({'error': '只有草稿或已驳回状态的计划才能提交'}), 400
    # if plan.plan_status != 'draft':
    #     return jsonify({'error': '仅草稿可提交'}), 400

    plan.plan_status = 'pending'
    db.session.commit()
    return jsonify({'message': '计划已提交'})

@plan_bp.route('/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id):
    data = request.get_json()
    plan = Plan.query.get_or_404(plan_id)

    try:
        plan.release_time = datetime.fromisoformat(data['release_time'].replace("Z", ""))
        plan.use_time = datetime.fromisoformat(data['use_time'].replace("Z", ""))
    except Exception as e:
        print('[ERROR] 时间解析失败:', e)
        return jsonify({'error': '时间格式不正确，请检查前端传参'}), 400

    plan.demand_id = data['demand_id']
    plan.user_id = data['user_id']
    plan.job_name = data['job_name']
    plan.recruit_number = data['recruit_number']
    # plan.release_time = datetime.fromisoformat(data['release_time'])
    # plan.use_time = datetime.fromisoformat(data['use_time'])
    plan.salary = data['salary']
    plan.plan_status = data['plan_status']

    db.session.commit()
    return jsonify({'code': 0, 'msg': '更新成功'})

# 删除计划
@plan_bp.route('/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    db.session.delete(plan)
    db.session.commit()
    return jsonify({'message': '计划已删除'})

# 获取通过的计划
@plan_bp.route('/options/approved', methods=['GET'])
def get_approved_plan_options():
    """
    返回 plan_status = 'approved' 的记录，格式：
      [{ label: plan.job_name, value: plan.plan_id }, ...]
    """
    approved_plans = Plan.query.filter_by(plan_status='approved').all()
    options = [
        {'label': plan.job_name, 'value': plan.plan_id}
        for plan in approved_plans
    ]
    return jsonify({'code': 0, 'data': options})