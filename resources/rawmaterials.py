from flask_restful import reqparse, Resource
from flask_jwt import jwt_required
from models.rawmaterials import RawmaterialModel
from models.controlnumber import ControlNumberModel

from flasgger import swag_from
import json
# from flask_restful_swagger_2 import Resource, swagger, Schema

# class BaseRawmaterialModel(Schema):
#     type = 'object'
#     properties = {
#         'control_no': {
#             'type': 'integer',
#             'format': 'int64',
#         }
#     }
#     required = ['control_no']

class Rawmaterial(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('control_no',
                        type=int,
                        required=True,
                        help="Every Rawmaterial needs a control_no.")
    parser.add_argument('check_year',
                        type=int,
                        required=True,
                        help="Every Rawmaterial needs a check year.")
    parser.add_argument('area_name',
                        type=str,
                        required=True,
                        help="Every Rawmaterial needs a area name.")
    parser.add_argument('process_no',
                        type=str,
                        required=True,
                        help="Every Rawmaterial needs a process no.")
    parser.add_argument('process_code',
                        type=int,
                        required=True,
                        help="Every Rawmaterial needs a process code.")
    parser.add_argument('equipment_no',
                        type=str,
                        required=True,
                        help="Every Rawmaterial needs a equipment no.")
    parser.add_argument('equipment_code',
                        type=int,
                        required=True,
                        help="Every Rawmaterial needs a equipment code.")
    parser.add_argument('raw_materials_code',
                        type=int,
                        required=True,
                        help="Every Rawmaterial needs a equipment no.")
    parser.add_argument('activity_data',
                        type=float,
                        required=True,
                        help="This activity_data field cannot be left blank!")
    parser.add_argument('activity_date',
                        type=str,
                        required=True,
                        help="Every Rawmaterial needs a activity date.")
    # parser.add_argument('control_no_id',
    #                     type=int,
    #                     required=True,
    #                     help="Every item needs a control no id.")

    @jwt_required()
    @swag_from('../docs/raematerial/raematerial.yaml')
    def post(self):
        # if RawmaterialModel.find_by_name(control_no):
        #     return {'message': "An rawmaterial with control_no '{}' already exists.".format(control_no)}, 400

        data = Rawmaterial.parser.parse_args()
        control_number = data["control_no"]

        # 查詢ControlNumberModel是否已有存在的Control number
        control_number_id = ControlNumberModel.find_by_name(str(control_number))
        if control_number_id:
            json_control_id = json.dumps(control_number_id.json())
            resp = json.loads(json_control_id)
            data["control_no_id"] = resp['id']
        # 沒有就新增一個Control number
        else:
            controlno = ControlNumberModel(control_number)
            try:
                controlno.save_to_db()
            except:
                return {'message': 'An error occurred while creating the control number.'}, 500

            new_json_control_id = json.dumps(controlno.json())
            new_resp = json.loads(new_json_control_id)
            data["control_no_id"] = new_resp['id']

        rawmaterial = RawmaterialModel(**data)

        try:
            rawmaterial.save_to_db()
        except:
            return {"message": "An error occurred inserting the rawmaterial."}, 500

        return {"message": "Inserting rawmaterial success!",
                "Rawmaterial": rawmaterial.json()}, 201

    def delete(self, control_no):
        rawmaterial = RawmaterialModel.find_by_name(control_no)
        if rawmaterial:
            rawmaterial.delete_from_db()

        return {'message': 'Rawmaterial deleted'}

    def put(self, control_no):
        data = Rawmaterial.parser.parse_args()

        rawmaterial = RawmaterialModel.find_by_name(control_no)

        if rawmaterial is None:
            rawmaterial = RawmaterialModel(control_no, **data)
        else:
            rawmaterial.control_no = data['control_no']
            rawmaterial.check_year = data['check_year']
            rawmaterial.area_name = data['area_name']
            rawmaterial.process_no = data['process_no']
            rawmaterial.process_code = data['process_code']
            rawmaterial.equipment_no = data['equipment_no']
            rawmaterial.equipment_code = data['equipment_code']
            rawmaterial.raw_materials_code = data['raw_materials_code']
            rawmaterial.activity_data = data['activity_data']
            rawmaterial.activity_date = data['activity_date']

        rawmaterial.save_to_db()

        return rawmaterial.json()


class RawmaterialList(Resource):    
    @swag_from('../docs/raematerial/raemateriallists.yaml')
    def get(self, control_number):
        rawmateriallists = RawmaterialModel.find_by_name(control_number)
        if rawmateriallists:
            return {'Rawmaterials': [rawmaterial.json() for rawmaterial in rawmateriallists]}
        return {'message': 'No Data'}, 404
        # return {'Rwmaterials': [x.json() for x in RawmaterialModel.query.all()]}
