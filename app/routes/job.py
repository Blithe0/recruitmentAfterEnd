from flask import Blueprint, request, jsonify
from app.services.job_service import get_all_jobs, create_job, update_job, delete_job
from app.schemas.job_schema import JobSchema

bp = Blueprint('job', __name__, url_prefix='/api/job')

@bp.route('', methods=['GET'])
def list_jobs():
    jobs = get_all_jobs()
    return jsonify(jobs)

@bp.route('', methods=['POST'])
def add_job():
    data = request.json
    job = create_job(data)
    return JobSchema().jsonify(job)

@bp.route('/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    data = request.json
    job = update_job(job_id, data)
    return JobSchema().jsonify(job)

@bp.route('/<int:job_id>', methods=['DELETE'])
def remove_job(job_id):
    delete_job(job_id)
    return '', 204
