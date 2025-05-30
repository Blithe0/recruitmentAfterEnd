from app.extensions import db
from datetime import datetime

class Plan(db.Model):
    __tablename__ = 'plan'

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    demand_id = db.Column(db.Integer, db.ForeignKey('demand.demand_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    recruit_number = db.Column(db.Integer, nullable=False)
    release_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    use_time = db.Column(db.DateTime, nullable=False)
    salary = db.Column(db.String(45), nullable=False)
    plan_status = db.Column(db.Enum('draft', 'pending', 'approved', 'rejected'), default='draft', nullable=False)
    job_name = db.Column(db.String(45), nullable=False)

    demand = db.relationship("Demand", backref="plans")

    def to_dict(self):
        return {
            'plan_id': self.plan_id,
            'demand_id': self.demand_id,
            'user_id': self.user_id,
            'recruit_number': self.recruit_number,
            'release_time': self.release_time.strftime('%Y-%m-%d'),
            'use_time': self.use_time.strftime('%Y-%m-%d'),
            'salary': self.salary,
            'job_name': self.job_name,
            'plan_status': self.plan_status
        }