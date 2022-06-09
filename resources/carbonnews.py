from flask_restful import reqparse, Resource
from models.carbonnews import CarbonNewsModel
from flasgger import swag_from
from werkzeug.datastructures import FileStorage
import base64


class FindCrabonNewsByHashTag(Resource):
    @swag_from('../docs/carbonnews/findcrabonnewsbyhashtag.yml')
    def get(self, hashtag=None):
        carbon_news = CarbonNewsModel.find_by_hash_tag(hashtag)
        if carbon_news:
            return [x.json() for x in carbon_news]
        return {'message': 'carbon news with hash tag not found'}, 404

class FindCrabonNewsByTitle(Resource):
    @swag_from('../docs/carbonnews/findcrabonnewsbytitle.yaml')
    def get(self, title=None):
        carbon_news = CarbonNewsModel.find_by_name(title)
        if carbon_news:
            return [x.json() for x in carbon_news]
        return {'message': 'carbon news with title not found'}, 404

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
    def get(self):
        return {'Carbon News List': [x.json() for x in CarbonNewsModel.query.all()]}
