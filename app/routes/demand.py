# app/routes/demand.py
from flask import Blueprint, request, jsonify
from app.models.demand import Demand
from app.extensions import db

demand_bp = Blueprint('demand', __name__, url_prefix='/api/demand')

# 获取所有需求
@demand_bp.route('/', methods=['GET'])
def get_all_demands():
    return jsonify([d.to_dict() for d in Demand.query.all()])

# 获取指定需求
@demand_bp.route('/<int:demand_id>', methods=['GET'])
def get_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    return jsonify(demand.to_dict())

# 创建招聘需求
@demand_bp.route('/', methods=['POST'])
def create_demand():
    data = request.get_json()
    demand = Demand(
        # department_id=data['department_id'],
        job_name=data['job_name'],
        job_type=data['job_type'],
        job_place=data['job_place'],
        demand_number=data['demand_number'],
        job_description=data['job_description'],
        job_requirement=data['job_requirement'],
        reason=data['reason'],
        demand_status='draft'
    )
    db.session.add(demand)
    db.session.commit()
    return jsonify({'message': '招聘需求已创建'}), 201

# 修改草稿状态的招聘需求
@demand_bp.route('/<int:demand_id>', methods=['PUT'])
def update_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    if demand.demand_status != 'draft':
        return jsonify({'error': '已提交的需求不可编辑'}), 400

    data = request.get_json()
    for field in [
        'job_name', 'job_type', 'job_place', 'demand_number',
        'job_description', 'job_requirement', 'reason'
    ]:
        if field in data:
            setattr(demand, field, data[field])

    db.session.commit()
    return jsonify({'message': '更新成功'})

# 删除草稿状态的招聘需求
@demand_bp.route('/<int:demand_id>', methods=['DELETE'])
def delete_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    if demand.demand_status != 'draft':
        return jsonify({'error': '已提交的需求不可删除'}), 400

    db.session.delete(demand)
    db.session.commit()
    return jsonify({'message': '删除成功'})

# 提交草稿状态的招聘需求
@demand_bp.route('/<int:demand_id>/submit', methods=['POST'])
def submit_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    if demand.demand_status != 'draft':
        return jsonify({'error': '仅草稿可提交'}), 400

    demand.demand_status = 'submitted'
    db.session.commit()
    return jsonify({'message': '需求已提交'})
