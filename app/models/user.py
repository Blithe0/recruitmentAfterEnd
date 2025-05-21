# app/models/user.py
from app.extensions import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(45), nullable=False)
    user_password = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.Integer, nullable=False)
    user_phone = db.Column(db.String(45))
    user_card = db.Column(db.String(45))
    user_sex = db.Column(db.String(45))

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_role': self.user_role,
            'user_phone': self.user_phone,
            'user_card': self.user_card,
            'user_sex': self.user_sex
        }