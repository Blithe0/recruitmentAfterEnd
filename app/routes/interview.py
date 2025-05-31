from flask import Blueprint, request, jsonify
from app.models.interview import Interview
from app.utils.mail import send_invitation_email
from app.extensions import db
import uuid

interview_bp = Blueprint('interview', __name__, url_prefix='/api/interview')

def generate_interview_link():
    return f"https://meeting.example.com/{uuid.uuid4()}"

@interview_bp.route('/', methods=['POST'])
def create_interview():
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
        email_sent=False  # 初始未发送邮件
    )
    db.session.add(interview)
    db.session.commit()

    return jsonify({
        'code': 0,
        'msg': '面试安排成功',
        'data': interview.to_dict()
    })


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
