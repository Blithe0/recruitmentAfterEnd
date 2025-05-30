from app.extensions import db
from sqlalchemy.dialects.mysql import ENUM, JSON

class Resume(db.Model):
    __tablename__ = 'resume'

    resume_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(ENUM('男', '女'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.Text)
    job_target = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    file_path = db.Column(db.String(255))
    parse_json = db.Column(JSON)
    status = db.Column(ENUM('pending', 'pass', 'reject'), default='pending')

    def to_dict(self):
        return {
            'resume_id': self.resume_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'degree': self.degree,
            'skills': self.skills,
            'job_target': self.job_target,
            'phone': self.phone,
            'email': self.email,
            'file_path': self.file_path,
            'parse_json': self.parse_json,
            'status': self.status
        }
