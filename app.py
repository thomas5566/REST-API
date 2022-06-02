import config.envvalues as CONFIGS

from flask import Flask
# from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.rawmaterials import Rawmaterial, RawmaterialList
from resources.controlnumber import ControlNumber, ControlNumberList, GetRawmaterialsListbyControlNumber
from resources.device import AddDevice
from resources.carbonnews import CarbonNews, CarbonNewslList, FindCrabonNewsByHashTag

from flask_cors import CORS
from flask_restful_swagger_2 import Api

from db import db

app = Flask(__name__)

# After creating the Flask app, you can make all APIs allow cross-origin access.
CORS(app)

security = {
    "appKey": {
        'in': 'header',
        'type': 'apiKey',
        'name': 'X-APP-KEY'
    }
}

app.config.from_object(CONFIGS)
app.secret_key = 'thomas'

api = Api(app,
          # host="localhost:5000",
          title='Rawmaterials API',
          schemes=['http'],
          # schemes=['https'],
          # base_path='/dev',
          security_definitions=security,
          security=[{'appKey': []}],
          api_version='0.01',
          api_spec_url='/api/swagger')

jwt = JWT(app, authenticate, identity)  # /auth

# Swagger(app, config=swagger_config, template=template)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ControlNumber, '/controlnumber/<string:control_number>')
api.add_resource(Rawmaterial, '/rawmaterial/<string:control_no>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(RawmaterialList, '/rawmaterials')
api.add_resource(ControlNumberList, '/controlnumbers')
api.add_resource(GetRawmaterialsListbyControlNumber, '/getrawbycontrolno/<string:control_number>')
api.add_resource(UserRegister, '/register')
api.add_resource(AddDevice, '/user/add-device')
api.add_resource(CarbonNews, '/carbonnews')
api.add_resource(FindCrabonNewsByHashTag, '/carbonnews/hashtag/<string:hashtag>')
api.add_resource(CarbonNewslList, '/carbonnews-lists')

db.init_app(app)

@app.route('/')
def index():
    return """<head>
    <meta http-equiv="refresh" content="0; url=http://petstore.swagger.io/?url=http://localhost:5000/api/swagger.json" />
    </head>"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
