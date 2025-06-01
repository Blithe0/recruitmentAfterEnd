# app/routes/resume.py
import os
import re
import pdfplumber
from flask import Blueprint, request, jsonify
from app.models.resume import Resume
from app.models.plan import Plan
from app.models.demand import Demand
from app.extensions import db

resume_bp = Blueprint('resume', __name__, url_prefix='/api/resume')

# 简单正则提取核心字段
def quick_parse(text: str) -> dict:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = lines[0] if lines else ''

    gender_m = re.search(r'性别[:：]?\s*(男|女)', text)
    gender = gender_m.group(1) if gender_m else ''

    age_m = re.search(r'年龄[:：]?\s*(\d{2,3})', text)
    age = age_m.group(1) if age_m else ''

    edu_m = re.search(r'学历[:：]?\s*(本科|硕士|博士|研究生)', text)
    education = edu_m.group(1) if edu_m else ''

    # 技能关键词库
    skill_keywords = [
        'HTML', 'CSS', 'JavaScript', 'Java', 'Python', 'Vue', 'SpringBoot', 'Pytorch',
        'MySQL', 'Linux', 'Docker', 'K8s', 'JMeter', 'Postman', 'Axure', 'Figma', 'NLP'
    ]
    matched_skills = []
    for kw in skill_keywords:
        if re.search(rf'\b{re.escape(kw)}\b', text, re.IGNORECASE):
            matched_skills.append(kw)

    skills = '、'.join(matched_skills)

    return {
        'name': name,
        'gender': gender,
        'age': age,
        'education': education,
        'skills': skills
    }
# def quick_parse(text: str) -> dict:
#     # 1) 姓名：第一行中文字符（假定）
#     lines = [l.strip() for l in text.splitlines() if l.strip()]
#     name = lines[0] if lines else ''
#
#     # 2) 年龄：找 两位或三位数字 + 岁
#     age_m = re.search(r'(\d{2,3})\s*岁', text)
#     age = age_m.group(1) if age_m else ''
#
#     # 3) 学历：本科/硕士/博士
#     edu_m = re.search(r'(本科|硕士|博士)', text)
#     education = edu_m.group(1) if edu_m else ''
#
#     # 4) 学校：中文+大学
#     school_m = re.search(r'([\u4e00-\u9fa5]+大学)', text)
#     school = school_m.group(1) if school_m else ''
#
#     # 5) 工龄：(\d+)年工作
#     work_m = re.search(r'(\d+)\s*年', text)
#     work_time = work_m.group(1) if work_m else ''
#
#     # 6) 意向岗位：找 “意向岗位[:：]\s*(.+?)\s*(\n|$)”
#     pos_m = re.search(r'意向岗位[:：]\s*(.+?)(?:\s|$|\n)', text)
#     match_position = pos_m.group(1).strip() if pos_m else ''
#     return {
#         'name': name,
#         'age': age,
#         'education': education,
#         'school': school,
#         'work_time': work_time,
#         'match_position': match_position
#     }

@resume_bp.route('/upload', methods=['POST'])
def upload_resume():
    file = request.files['file']
    upload_dir = os.path.join(os.getcwd(), 'app', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)

    # 抽取文本
    with pdfplumber.open(file_path) as pdf:
        text = ''.join(page.extract_text() or '' for page in pdf.pages)
        print(text)

    # 正则快速解析
    entities = quick_parse(text)

    # 入库
    resume = Resume(
        name=entities['name'],
        age=int(entities['age']) if entities['age'].isdigit() else None,
        degree=entities['education'],
        job_target=entities.get('match_position', ''),  # 原代码有误
        skills=entities.get('skills', '[]'),  # 这里改成提取 skills
        gender=entities.get('gender', '未知'),
        phone='',
        email='',
        file_path=file_path,
        parse_json=entities,
        status='pending'
    )
    # resume = Resume(
    #     name=entities['name'],
    #     age=int(entities['age']) if entities['age'].isdigit() else None,
    #     degree=entities['education'],
    #     job_target=entities['match_position'],
    #     skills='[]',
    #     gender='未知',
    #     phone='',
    #     email='',
    #     file_path=file_path,
    #     parse_json=entities,
    #     status='pending'
    # )
    db.session.add(resume)
    db.session.commit()

    # return jsonify({'code': 0, 'msg': '上传并解析成功', 'data': entities}), 200
    return jsonify({'code': 0, 'msg': '上传并解析成功', 'data': resume.to_dict()}), 200

@resume_bp.route('/', methods=['GET'])
def get_resume_list():
    resumes = Resume.query.all()
    return jsonify([r.to_dict() for r in resumes])

@resume_bp.route('/<int:resume_id>', methods=['DELETE'])
def delete_resume(resume_id):
    r = Resume.query.get_or_404(resume_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'msg': '删除成功'}), 200

# 修改简历状态
@resume_bp.route('/<int:resume_id>/status', methods=['PUT'])
def update_resume_status(resume_id):
    data = request.get_json()
    new_status = data.get('status')
    if new_status not in ['pending', 'pass', 'reject']:
        return jsonify({'code': 1, 'msg': '非法状态值'})

    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'code': 1, 'msg': '未找到简历'})

    # 如果已审核，则不能再次修改
    if resume.status != 'pending':
        return jsonify({'code': 1, 'msg': '该简历已审核，不能再次修改'})

    resume.status = new_status
    db.session.commit()
    return jsonify({'code': 0, 'msg': '状态更新成功'})

# @resume_bp.route('/<int:resume_id>/status', methods=['PATCH'])
# def update_status(resume_id):
#     r = Resume.query.get_or_404(resume_id)
#     s = request.json.get('status')
#     if s not in ('pending','pass','reject'):
#         return jsonify({'error':'无效状态'}),400
#     r.status = s
#     db.session.commit()
#     return jsonify({'msg':'更新成功'}),200

# 获取通过简历
@resume_bp.route('/approved', methods=['GET'])
def get_approved_candidates():
    resumes = Resume.query.filter_by(status='pass').all()
    data = [
        {
            'label': r.name,
            'value': r.resume_id
        }
        for r in resumes
    ]
    return jsonify({'code': 0, 'data': data})




@resume_bp.route('/<int:resume_id>/match', methods=['GET'])
def match_resume(resume_id):
    """
    将简历中提取出的 skills 与所有 plan_status='approved' 的招聘计划对应的
    Demand.job_requirement 进行关键词匹配，返回匹配数量最高的前三个岗位(计划)。
    """
    # 1. 找到 resume
    resume = Resume.query.get_or_404(resume_id)

    # 2. 拆分技能列表 (假设 Resume.skills 存储类似 "HTML、CSS、JavaScript、Python" 的字符串)
    raw_skills = resume.skills or ''
    skills_list = [s.strip() for s in raw_skills.split('、') if s.strip()]

    # 3. 查询所有 plan_status='approved' 的 Plan，并关联对应的 Demand
    approved_plans = Plan.query.filter_by(plan_status='approved').all()

    matches = []
    for plan in approved_plans:
        demand = Demand.query.get(plan.demand_id)
        if not demand:
            continue
        job_req = demand.job_requirement or ''
        # 4. 统计该需求描述中每个技能出现的次数（这里只做简单 substring 判断）
        count = 0
        for skill in skills_list:
            if skill and skill in job_req:
                count += 1
        matches.append({
            'plan_id': plan.plan_id,
            'job_name': demand.job_name,            # 最终返回给前端的“岗位名称”
            'match_count': count                     # 匹配到的技能数量
        })

    # 5. 按照 match_count 从大到小排序，取前 3 条
    matches_sorted = sorted(matches, key=lambda x: x['match_count'], reverse=True)
    top3 = matches_sorted[:3]

    return jsonify({'code': 0, 'data': top3})

