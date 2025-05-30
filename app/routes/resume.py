from flask import Blueprint, request, jsonify
from app.models.resume import Resume
from app.extensions import db
from app.schemas.resume import ResumeCreateSchema, ResumeUpdateSchema
from pydantic import ValidationError

from app.resume_parser.parser_model import predict

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

# 获取所有简历
@resume_bp.route('/', methods=['GET'])
def get_all_resumes():
    resumes = Resume.query.all()
    return jsonify([r.to_dict() for r in resumes])

# 添加简历
@resume_bp.route('/', methods=['POST'])
def create_resume():
    try:
        data = ResumeCreateSchema(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    resume = Resume(**data.dict())
    db.session.add(resume)
    db.session.commit()
    return jsonify({'message': '简历创建成功', 'resume_id': resume.resume_id}), 201

# 更新简历状态或信息
@resume_bp.route('/<int:resume_id>', methods=['PUT'])
def update_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    try:
        data = ResumeUpdateSchema(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    for field, value in data.dict(exclude_unset=True).items():
        setattr(resume, field, value)

    db.session.commit()
    return jsonify({'message': '简历更新成功'})

# 删除简历
@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    db.session.delete(resume)
    db.session.commit()
    return jsonify({'message': '简历已删除'})

@resume_bp.route('/parse', methods=['POST'])
def parse_resume():
    content = request.json.get('text', '')
    if not content:
        return jsonify({'error': 'No text provided'}), 400
    parsed = predict(content)
    return jsonify({'parsed': parsed})
# def parse_resume():
#     file_path = request.json.get('file_path')
#     if not file_path or not os.path.exists(file_path):
#         return jsonify({'msg': '文件路径无效'}), 400
#
#     parser = ResumeParser()
#     result = parser.parse(file_path)  # 返回结构化json
#     return jsonify(result)
