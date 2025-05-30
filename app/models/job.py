from app.extensions import db

class Job(db.Model):
    __tablename__ = 'job'

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    pass_number = db.Column(db.Integer, default=0)
    job_status = db.Column(db.Enum('draft', 'recruiting', 'stop'), default='draft')

    plan = db.relationship('Plan', backref=db.backref('job', uselist=False))
