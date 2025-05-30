import os
import uuid
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.resume import Resume
from app.resume_parser.parser_model import parse_resume_pdf  # 你自定义的简历解析工具

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads/resumes')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 上传简历并解析
@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.pdf'):
        return jsonify({'code': 1, 'msg': '仅支持PDF文件'}), 400

    # 保存文件
    filename = f"{uuid.uuid4().hex}.pdf"
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    # 解析PDF内容并提取结构化信息
    parse_result = parse_resume_pdf(save_path)
    # parse_result: dict, 比如 {name: ..., gender: ..., ...}
    if not parse_result:
        return jsonify({'code': 2, 'msg': '解析失败'}), 400

    # 构建Resume对象，部分字段允许为空
    resume = Resume(
        name=parse_result.get('name', ''),
        gender=parse_result.get('gender', ''),
        age=parse_result.get('age', 0),
        degree=parse_result.get('degree', ''),
        skills=parse_result.get('skills', ''),
        job_target=parse_result.get('job_target', ''),
        phone=parse_result.get('phone', ''),
        email=parse_result.get('email', ''),
        file_path=f'/uploads/resumes/{filename}',
        parse_json=parse_result,
        status='pending'
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify({'code': 0, 'msg': '上传成功', 'data': resume.to_dict()})
