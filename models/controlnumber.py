from db import db


class ControlNumberModel(db.Model):
    __tablename__ = 'controlnumbers'

    id = db.Column(db.Integer, primary_key=True)
    control_number = db.Column(db.String(80))
    
    rawmaterials = db.relationship('RawmaterialModel', lazy='dynamic') # List of the items ex. one store have many items

    def __init__(self, control_number):
        self.control_number = control_number

    def json(self):
        return {
            'control_number': self.control_number,
            'rawmaterials': [rawmaterial.json() for rawmaterial in self.rawmaterials.all()]
            }

    @classmethod
    def find_by_name(cls, control_number):
        return cls.query.filter_by(control_number=control_number).first()

    @classmethod
    def find_rawmaterials_by_controlnumber(cls, control_number):
        return cls.query.filter_by(control_number=control_number).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()