from flask import request
from flask_restful import reqparse
from models.carbonnews import CarbonNewsModel

from flask_restful_swagger_2 import Resource, swagger, Schema
from werkzeug.datastructures import FileStorage
import base64

class BaseCarbonNewsModel(Schema):
    type = 'object'
    properties = {
        'hashtag': {
            'type': 'string',
            'format': 'str',
        }
    }
    required = ['hashtag']


class FindCrabonNewsByHashTag(Resource):
    @swagger.doc({
        'tags': ['Carbon News'],
        'description': 'Search Carbon News with hash-tag',
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
                'schema': BaseCarbonNewsModel,
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
    def get(self, hashtag=None):
        carbon_news = CarbonNewsModel.find_by_hash_tag(hashtag)
        if carbon_news:
            return [x.json() for x in carbon_news]
        return {'message': 'carbon news with hash tag not found'}, 404

class CarbonNews(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True,
                        help="Every Carbon News needs a title.")
    parser.add_argument('content', type=str, required=True,
                        help="Every Carbon News needs contents.")
    parser.add_argument('sourceurl', type=str)
    parser.add_argument('sourcedescription', type=str)
    parser.add_argument('eventdate', type=str, required=True,
                        help="Every Carbon News needs a event date.")
    parser.add_argument('comment', type=str)
    parser.add_argument('suggest', type=str)
    parser.add_argument('speakingnote', type=str)
    parser.add_argument('hashtag', type=str, required=True,
                        help="Every Carbon News needs a hash tag.")
    parser.add_argument('newsimage', type=FileStorage, location='files')

    @swagger.doc({
        'tags': ['Carbon News'],
        'description': 'Search Carbon News with hash-tag',
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
                'schema': BaseCarbonNewsModel,
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
    def get(self, title=None):
        carbon_news = CarbonNewsModel.find_by_name(title)
        if carbon_news:
            return [x.json() for x in carbon_news]
        return {'message': 'carbon news with title not found'}, 404

    @swagger.doc({
        'tags': ['Carbon News'],
        'description': 'Adds a Carbon News',
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
    def post(self):
        data = CarbonNews.parser.parse_args()

        if CarbonNewsModel.find_by_name(data['title']):
            return {'message': "An Carbon News with title '{}' already exists.".format(data['title'])}, 400

        encoded_string = base64.b64encode(data['newsimage'].read()).decode('utf-8')
        if encoded_string:
            data['newsimage'] = encoded_string

        carbon_news = CarbonNewsModel(**data)

        try:
            carbon_news.save_to_db()
        except:
            return {"message": "An error occurred inserting the carbon news."}, 500

        return {"message": "Inserting carbon news success!", "carbon_news": carbon_news.json()}, 201

    def delete(self, title):
        carbon_news = CarbonNewsModel.find_by_name(title)
        if carbon_news:
            carbon_news.delete_from_db()

        return {'message': 'Carbon news deleted'}

    def put(self, title):
        data = CarbonNews.parser.parse_args()

        carbon_news = CarbonNewsModel.find_by_name(title)

        if carbon_news is None:
            carbon_news = CarbonNewsModel(**data)
        else:
            carbon_news.title = data['title']
            carbon_news.content = data['content']
            carbon_news.sourceurl = data['sourceurl']
            carbon_news.sourcedescription = data['sourcedescription']
            carbon_news.eventdate = data['eventdate']
            carbon_news.comment = data['comment']
            carbon_news.suggest = data['suggest']
            carbon_news.speakingnote = data['speakingnote']
            carbon_news.hashtag = data['hashtag']
            carbon_news.newsimage = data['newsimage']

        carbon_news.save_to_db()

        return carbon_news.json()


class CarbonNewslList(Resource):
    @swagger.doc({
        'tags': ['Carbon News'],
        'description': 'Get all rawmaterials',
        'responses': {
            '200': {
                'description': 'Control number',
                'schema': BaseCarbonNewsModel,
                # 'examples': {
                #     'application/json': [
                #         {
                #             "control_no": "11880755",
                #             "check_year": 2022,
                #             "area_name": "5566",
                #             "process_no": "7788",
                #             "process_code": 7788,
                #             "equipment_no": "7788",
                #             "equipment_code": 445566,
                #             "raw_materials_code": 11880755,
                #             "activity_data": 15.9999999,
                #             "activity_date": "2022/05/19"
                #         },
                #         {
                #             "control_no": "5566",
                #             "check_year": 2022,
                #             "area_name": "5566",
                #             "process_no": "7788",
                #             "process_code": 7788,
                #             "equipment_no": "7788",
                #             "equipment_code": 445566,
                #             "raw_materials_code": 11880755,
                #             "activity_data": 15.9999999,
                #             "activity_date": "2022/05/19"
                #         }
                #     ]
                # }
            }
        }
     })
    def get(self):
        return {'Carbon News List': [x.json() for x in CarbonNewsModel.query.all()]}
