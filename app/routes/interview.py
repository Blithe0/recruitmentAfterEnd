from flask import Blueprint, request, jsonify
from app.models.interview import Interview
from app.utils.mail import send_invitation_email
from app.extensions import db
import uuid

interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')

def generate_interview_link():
    return f"https://meeting.example.com/{uuid.uuid4()}"

# 创建
@interview_bp.route('/', methods=['POST'])
def create_interview():
    try:
        data = request.json

        if not data.get("interviewer_time"):
            return jsonify({'code': 1, 'msg': '面试时间不能为空'}), 400

        interview = Interview(
            candidate_id=data['candidate_id'],
            interviewer_id=data['interviewer_id'],
            user_id=data['user_id'],
            job_id=data['job_id'],
            interviewer_time=data['interviewer_time'],
            interview_type=data['interview_type'],
            interview_link=generate_interview_link(),
            email_sent=False
        )
        db.session.add(interview)
        db.session.commit()

        return jsonify({
            'code': 0,
            'msg': '面试安排成功',
            'data': interview.to_dict()
        })

    except Exception as e:
        print("创建面试失败：", str(e))
        return jsonify({'code': 500, 'msg': '服务器错误', 'error': str(e)}), 500

@interview_bp.route('/<int:id>', methods=['PUT'])
def update_interview(id):
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({'code': 1, 'msg': '该面试记录不存在'}), 404

    data = request.json

    # 字段更新
    interview.candidate_id = data.get('candidate_id', interview.candidate_id)
    interview.interviewer_id = data.get('interviewer_id', interview.interviewer_id)
    interview.user_id = data.get('user_id', interview.user_id)
    interview.job_id = data.get('job_id', interview.job_id)
    interview.interviewer_time = data.get('interviewer_time', interview.interviewer_time)
    interview.interview_type = data.get('interview_type', interview.interview_type)

    db.session.commit()

    return jsonify({'code': 0, 'msg': '更新成功', 'data': interview.to_dict()})

@interview_bp.route('/<int:id>', methods=['DELETE'])
def delete_interview(id):
    interview = Interview.query.get(id)
    if not interview:
        return jsonify({'code': 1, 'msg': '面试记录不存在'}), 404
    if interview.email_sent:
        return jsonify({'code': 1, 'msg': '通知已发送，无法删除'}), 403

    db.session.delete(interview)
    db.session.commit()
    return jsonify({'code': 0, 'msg': '删除成功'})

@interview_bp.route('/list', methods=['GET'])
def list_interviews():
    interviews = Interview.query.order_by(Interview.interview_id.desc()).all()
    data = [interview.to_dict() for interview in interviews]
    return jsonify({'code': 0, 'msg': '获取成功', 'data': data})


@interview_bp.route('/send_email', methods=['POST'])
def send_interview_email():
    data = request.json
    interview = Interview.query.get(data.get('interview_id'))

    if not interview:
        return jsonify({'code': 1, 'msg': '面试不存在'})

    # 发送邮件
    send_invitation_email(
        candidate_id=interview.candidate_id,
        interviewer_id=interview.interviewer_id,
        time=interview.interviewer_time,
        method=interview.interview_type,
        link=interview.interview_link
    )

    # 标记已发送
    interview.email_sent = True
    db.session.commit()

    return jsonify({'code': 0, 'msg': '邮件发送成功'})
