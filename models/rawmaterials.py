from db import db

class RawmaterialModel(db.Model):
    __tablename__ = 'CompanyRawMaterialsAPI'

    id = db.Column(db.Integer, primary_key=True)
    control_no = db.Column(db.String(80), default=None)
    check_year = db.Column(db.Integer, default=None)
    area_name = db.Column(db.String(80), default=None)
    process_no = db.Column(db.String(80), default=None)
    process_code = db.Column(db.Integer, default=None)
    equipment_no = db.Column(db.String(80), default=None)
    equipment_code = db.Column(db.Integer, default=None)
    raw_materials_code = db.Column(db.Integer, default=None)
    activity_data = db.Column(db.Float(precision=10), default=None)
    activity_date = db.Column(db.String(80), default=None)

    control_no_id = db.Column(db.Integer, db.ForeignKey('controlnumbers.id'))
    control_number = db.relationship('ControlNumberModel')

    def __init__(self, control_no, check_year, area_name
                     , process_no, process_code
                     , equipment_no, equipment_code
                     , raw_materials_code
                     , activity_data, activity_date
                     , control_no_id):
        self.control_no = control_no
        self.check_year = check_year
        self.area_name = area_name
        self.process_no = process_no
        self.process_code = process_code
        self.equipment_no = equipment_no
        self.equipment_code = equipment_code
        self.raw_materials_code = raw_materials_code
        self.activity_data = activity_data
        self.activity_date = activity_date
        self.control_no_id = control_no_id

    def json(self):
        return {'control_no': self.control_no, 'check_year': self.check_year
                , 'area_name': self.area_name
                , 'process_no': self.process_no, 'process_code': self.process_code
                , 'equipment_no': self.equipment_no, 'equipment_code': self.equipment_code
                , 'raw_materials_code': self.raw_materials_code
                , 'activity_data': self.activity_data
                , 'activity_date': self.activity_date
                }

    @classmethod
    def find_by_name(cls, control_no):
        return cls.query.filter_by(control_no=control_no).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()