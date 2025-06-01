from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.job import Job
from app.models.plan import Plan
from datetime import datetime

job_bp = Blueprint('job', __name__, url_prefix='/api/job')


@job_bp.route('', methods=['GET'])
def get_job_list():
    jobs = Job.query.all()
    job_list = []
    for job in jobs:
        plan = Plan.query.get(job.plan_id)
        job_list.append({
            'job_id': job.job_id,
            'plan_id': job.plan_id,
            'user_id': job.user_id,
            'pass_number': job.pass_number,
            'job_status': job.job_status,
            # 从 plan 引用字段
            'job_name': plan.job_name if plan else '',
            'recruit_number': plan.recruit_number if plan else 0,
            'job_place': plan.demand.job_place if plan and plan.demand else '',
            'job_description': plan.demand.job_description if plan and plan.demand else '',
            'job_requirement': plan.demand.job_requirement if plan and plan.demand else '',
            # 'job_place': plan.job_place if plan else '',
            # 'job_description': plan.job_description if plan else '',
            # 'job_requirement': plan.job_requirement if plan else '',
            'salary': plan.salary if plan else '',
            'release_time': plan.release_time.strftime('%Y-%m-%d') if plan and plan.release_time else '',
            'use_time': plan.use_time.strftime('%Y-%m-%d') if plan and plan.use_time else ''
        })
    return jsonify(job_list)


@job_bp.route('', methods=['POST'])
def create_job():
    data = request.json
    job = Job(
        plan_id=data['plan_id'],
        user_id=data['user_id'],
        pass_number=data.get('pass_number', 0),
        job_status='draft'
    )
    db.session.add(job)
    db.session.commit()
    return jsonify({'message': '岗位创建成功'}), 201


@job_bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    data = request.json
    job.pass_number = data.get('pass_number', job.pass_number)
    job.job_status = data.get('job_status', job.job_status)
    db.session.commit()
    return jsonify({'message': '岗位信息更新成功'})


@job_bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return jsonify({'message': '岗位删除成功'})


@job_bp.route('/<int:job_id>/publish', methods=['POST'])
def publish_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.job_status != 'draft':
        return jsonify({'error': '只能发布草稿状态的岗位'}), 400
    job.job_status = 'recruiting'
    db.session.commit()
    return jsonify({'message': '岗位已发布'})


@job_bp.route('/<int:job_id>/stop', methods=['POST'])
def stop_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.job_status != 'recruiting':
        return jsonify({'error': '只能停止招聘中状态的岗位'}), 400
    job.job_status = 'stop'
    db.session.commit()
    return jsonify({'message': '岗位已停止招聘'})

@job_bp.route('/<int:job_id>/recover', methods=['POST'])
def recover_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    if job.job_status != 'stop':
        return jsonify({'error': 'Only stopped jobs can be recovered'}), 400

    job.job_status = 'recruiting'
    db.session.commit()
    return jsonify({'message': 'Job recovered to recruiting status'}), 200


@job_bp.route('/options', methods=['GET'])
def get_job_options():
    jobs = Job.query.all()
    data = [
        {
            'label': job.plan.job_name,
            'value': job.job_id
        }
        for job in jobs
    ]
    return jsonify({'code': 0, 'data': data})

# 获取发布岗位信息
@job_bp.route('/released', methods=['GET'])
def get_released_jobs():
    jobs = Job.query.filter_by(job_status='released').all()
    job_list = [{'label': job.job_name, 'value': job.job_id} for job in jobs]
    return jsonify({'code': 0, 'msg': '获取成功', 'data': job_list})
