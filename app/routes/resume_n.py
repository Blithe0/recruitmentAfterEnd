import requests
import pdfplumber
from flask import Blueprint, request, jsonify
from app.models.resume import Resume
from app.extensions import db

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['file']
    file_path = f'uploads/{file.filename}'
    file.save(file_path)

    # 提取文本
    with pdfplumber.open(file_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)

    # 调用微服务解析字段
    resp = requests.post('http://localhost:5001/predict', json={'text': text})
    entities = resp.json()

    # 存储数据库
    resume = Resume(
        name=entities.get('name', ''),
        age=int(entities.get('age', 0)),
        degree=entities.get('education', ''),
        job_target=entities.get('match_position', ''),
        skills='[]',
        gender='男',
        phone='',
        email='',
        file_path=file_path,
        parse_json=entities,
        status='pending'
    )
    db.session.add(resume)
    db.session.commit()

    return jsonify({'msg': '上传成功', 'data': entities}), 200
