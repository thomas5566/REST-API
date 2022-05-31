from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.rawmaterials import RawmaterialModel

from flask_restful_swagger_2 import Resource, swagger, Schema

class BaseRawmaterialModel(Schema):
    type = 'object'
    properties = {
        'control_no': {
            'type': 'integer',
            'format': 'int64',
        }
    }
    required = ['control_no']

class Rawmaterial(Resource):
    parser = reqparse.RequestParser()
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
    parser.add_argument('control_no_id',
                        type=int,
                        required=True,
                        help="Every item needs a control no id.")

    @swagger.doc({
        'tags': ['Rawmaterial'],
        'description': 'Returns a latest rawmaterial',
        'parameters': [
            {
                'name': 'control_no',
                'description': 'Control number',
                'in': 'path',
                'type': 'integer'
            }
        ],
        'responses': {
            '200': {
                'description': 'Control number',
                'schema': BaseRawmaterialModel,
                'examples': {
                    'application/json': {
                        "control_no": "11880755",
                        "check_year": 2022,
                        "area_name": "5566",
                        "process_no": "7788",
                        "process_code": 7788,
                        "equipment_no": "7788",
                        "equipment_code": 445566,
                        "raw_materials_code": 11880755,
                        "activity_data": 15.9999999,
                        "activity_date": "2022/05/19"
                    }
                }
            }
        }
     })
    def get(self, control_no):
        rawmaterial = RawmaterialModel.find_by_name(control_no)
        if rawmaterial:
            return rawmaterial.json()
        return {'message': 'rawmaterial not found'}, 404

    @swagger.doc({
        'tags': ['Rawmaterial'],
        'description': 'Adds a Rawmaterial',
        'parameters': [            
            {
                'name': 'control_no',
                'description': 'Control number',
                'in': 'path',
                'type': 'integer',
            }
        ],
        'responses': {
            '201': {
                'description': 'Created Rawmaterial',
                'examples': {
                    'application/json': {
                        "check_year": 2024,
                        "area_name": "廠區A",
                        "process_no": "A1",
                        "process_code": 9999,
                        "equipment_no": "AA1",
                        "equipment_code": 88888,
                        "raw_materials_code": 445566,
                        "activity_data": 33.3333333,
                        "activity_date": "2022/05/23",
                        "control_no_id": 2
                    }
                }
            }
        }
    })
    @jwt_required()
    def post(self, control_no):
        # if RawmaterialModel.find_by_name(control_no):
        #     return {'message': "An rawmaterial with control_no '{}' already exists.".format(control_no)}, 400

        data = Rawmaterial.parser.parse_args()

        rawmaterial = RawmaterialModel(control_no, **data)

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
    @swagger.doc({
        'tags': ['Rawmaterial'],
        'description': 'Get all rawmaterials',        
        'responses': {
            '200': {
                'description': 'Control number',
                'schema': BaseRawmaterialModel,
                'examples': {
                    'application/json': [
                        {
                            "control_no": "11880755",
                            "check_year": 2022,
                            "area_name": "5566",
                            "process_no": "7788",
                            "process_code": 7788,
                            "equipment_no": "7788",
                            "equipment_code": 445566,
                            "raw_materials_code": 11880755,
                            "activity_data": 15.9999999,
                            "activity_date": "2022/05/19"
                        },
                        {
                            "control_no": "5566",
                            "check_year": 2022,
                            "area_name": "5566",
                            "process_no": "7788",
                            "process_code": 7788,
                            "equipment_no": "7788",
                            "equipment_code": 445566,
                            "raw_materials_code": 11880755,
                            "activity_data": 15.9999999,
                            "activity_date": "2022/05/19"
                        }
                    ]
                }
            }
        }
     })
    def get(self):
        return {'Rwmaterials': [x.json() for x in RawmaterialModel.query.all()]}
