from app.extensions import db
from sqlalchemy import Enum

INTERVIEW_TYPE_CHOICES = ('one', 'group', 'structured')

class Interview(db.Model):
    __tablename__ = 'interview'

    interview_id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, nullable=False)
    interviewer_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    job_id = db.Column(db.Integer, nullable=False)
    interviewer_time = db.Column(db.DateTime, nullable=False)
    interview_type = db.Column(db.Enum('one', 'group', 'structured'), nullable=False)
    # interview_type = db.Column(
    #     Enum(*INTERVIEW_TYPE_CHOICES, name='interview_type_enum'),
    #     nullable=False
    # )
    interview_link = db.Column(db.String(255), nullable=False)
    email_sent = db.Column(db.Boolean, default=False)  # 新增字段：邮件是否已发送

    def to_dict(self):
        return {
            'interview_id': self.interview_id,
            'candidate_id': self.candidate_id,
            'interviewer_id': self.interviewer_id,
            'user_id': self.user_id,
            'job_id': self.job_id,
            'interviewer_time': self.interviewer_time.isoformat(),
            'interview_type': self.interview_type,
            'interview_link': self.interview_link,
            'email_sent': self.email_sent
        }
