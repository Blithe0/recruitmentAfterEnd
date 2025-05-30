# app/routes/resume.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.resume import Resume
from app.schemas.resume import ResumeCreateSchema, ResumeResponseSchema
from app.resume_parser.parser_model import parse_resume_pdf
from pydantic import ValidationError

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@resume_bp.route('/', methods=['GET'])
def get_resume_list():
    resumes = Resume.query.all()
    return jsonify([ResumeResponseSchema(**r.to_dict()).dict() for r in resumes])

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    接收前端上传的文件（form-data => file），
    保存到本地，然后调用解析，最终写入 DB。
    """
    f = request.files.get('file')
    if not f:
        return jsonify({"error": "no file"}), 400

    # 1. 存储文件
    save_path = f"./uploads/{f.filename}"
    f.save(save_path)

    # 2. 解析
    data = parse_resume_pdf(save_path)

    # 3. 数据验证 & 存库
    try:
        schema = ResumeCreateSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    resume = Resume(**schema.dict())
    db.session.add(resume)
    db.session.commit()
    return jsonify({"message": "upload & parse success"}), 201

@resume_bp.route('/<int:resume_id>/status', methods=['PUT'])
def update_status(resume_id):
    json_in = request.get_json()
    resume = Resume.query.get_or_404(resume_id)
    resume.status = json_in.get('status', resume.status)
    db.session.commit()
    return jsonify({"message": "status updated"})
