from app.extensions import db
from sqlalchemy.dialects.mysql import JSON
from app.models.plan import Plan

class Selection(db.Model):
    __tablename__ = 'selection'
    selection_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=False)
    # steps_json = db.Column(db.JSON, nullable=False)
    steps_json = db.Column(JSON, nullable=False)

    # 建立与 Plan 表的关系
    # plan = db.relationship('Plan', backref=db.backref('selections', lazy='dynamic'))
    plan = db.relationship('Plan', backref=db.backref('selections', lazy=True))

    def to_dict(self):
        return {
            'id': self.selection_id,
            'plan_id': self.plan_id,
            'steps': self.steps_json
        }
