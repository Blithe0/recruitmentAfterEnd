from app.extensions import db

class Talent(db.Model):
    __tablename__ = 'talent'

    talent_id = db.Column(db.Integer, primary_key=True)
    talent_name = db.Column(db.String(45))
    talent_sex = db.Column(db.String(45))
    talent_type = db.Column(db.Integer)
    talent_phone = db.Column(db.String(45))
    talent_card = db.Column(db.String(45))

    def to_dict(self):
        return {
            'talent_id': self.talent_id,
            'talent_name': self.talent_name,
            'talent_sex': self.talent_sex,
            'talent_type': self.talent_type,
            'talent_phone': self.talent_phone,
            'talent_card': self.talent_card
        }
