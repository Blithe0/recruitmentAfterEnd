from app.extensions import db

class Interviewer(db.Model):
    __tablename__ = 'interviewer'

    interviewer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'interviewer_id': self.interviewer_id,
            'name': self.name,
            'department_id': self.department_id,
            'contact': self.contact
        }
