from app.extensions import db

class Selection(db.Model):
    __tablename__ = 'selection'

    selection_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    steps_json = db.Column(db.Text, nullable=False)  # 存储步骤的 JSON 字符串
