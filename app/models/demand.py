from app.extensions import db

class Demand(db.Model):
    __tablename__ = 'demand'
    demand_id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, nullable=False)
    job_name = db.Column(db.String(45), nullable=False)
    job_type = db.Column(db.Integer)
    job_place = db.Column(db.String(45))
    demand_number = db.Column(db.Integer)
    job_description = db.Column(db.String(255))
    job_requirement = db.Column(db.String(255))
    reason = db.Column(db.String(255))
    demand_status = db.Column(db.Enum('草稿', '已提交'), default='草稿')

    def to_dict(self):
        return {
            'demand_id': self.demand_id,
            'department_id': self.department_id,
            'job_name': self.job_name,
            'job_type': self.job_type,
            'job_place': self.job_place,
            'demand_number': self.demand_number,
            'job_description': self.job_description,
            'job_requirement': self.job_requirement,
            'reason': self.reason,
            'demand_status': self.demand_status
        }
