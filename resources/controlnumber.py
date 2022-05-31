from flask_restful import Resource
from models.controlnumber import ControlNumberModel

class ControlNumber(Resource):
    def get(self, control_number):
        controlno = ControlNumberModel.find_by_name(control_number)
        if controlno:
          return controlno.json()
        return {'message': 'Control number not found'}, 404
    
    def post(self, control_number):
        if ControlNumberModel.find_by_name(control_number):
            return {'message': "A control number with name '{}' already exists.".format(control_number)}, 400
        
        controlno = ControlNumberModel(control_number)
        try:
            controlno.save_to_db()
        except:
            return {'message': 'An error occurred while creating the control number.'}, 500
        
        return {'message': "Creat control number '{}' success!".format(control_number)}, 200
    
    def delete(self, control_number):
        controlno = ControlNumberModel.find_by_name(control_number)
        if controlno:
            controlno.delete_from_db()
            
        return {'message': 'Control number deleted'}
      
class ControlNumberList(Resource):
    def get(self):
        return {'ControlNumbers': [controlno.json() for controlno in ControlNumberModel.query.all()]}
                

class GetRawmaterialsListbyControlNumber(Resource):
    def get(self, control_number):
        controllists = ControlNumberModel.find_rawmaterials_by_controlnumber(control_number)
        if controllists:
            return {'ControlNumbers': [controlno.json() for controlno in controllists]}

        return {'message': 'No Data'}, 404