import config.envvalues as CONFIGS
import json
from config.swagger import template, swagger_config

from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt import JWT, JWTError
from flask_cors import CORS
from flasgger import Swagger, swag_from

from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.rawmaterials import Rawmaterial, RawmaterialList
from resources.controlnumber import ControlNumber, ControlNumberList, GetRawmaterialsListbyControlNumber
from resources.device import AddDevice
from resources.carbonnews import CarbonNews, CarbonNewslList, FindCrabonNewsByHashTag, FindCrabonNewsByTitle


app = Flask(__name__)
# After creating the Flask app, you can make all APIs allow cross-origin access.
CORS(app)

app.config.from_object(CONFIGS)

db.init_app(app)
app.secret_key = 'thomas5568'
api = Api(app, prefix='/api/v1')

@app.before_first_request
def create_tables():
    db.create_all()

def jwt_request_handler():
    auth_header_name = app.config['JWT_AUTH_HEADER_NAME']
    auth_header_value = request.headers.get(auth_header_name, None)
    auth_header_prefix = app.config['JWT_AUTH_HEADER_PREFIX']
    if not auth_header_value:
        return

    parts = auth_header_value.split()

    if parts[0].lower() != auth_header_prefix.lower():
        raise JWTError('Invalid JWT header', 'Unsupported authorization type')
    elif len(parts) == 1:
        raise JWTError('Invalid JWT header', 'Token missing')
    elif len(parts) > 2:
        raise JWTError('Invalid JWT header', 'Token contains spaces')

    return parts[1]

jwt = JWT(app, authenticate, identity)  # /auth
# jwt.request_handler(jwt_request_handler)

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    @swag_from('./docs/auth/login.yaml')
    def post(self):
        data = UserLogin.parser.parse_args()

        try:
            username = data["username"]
            password = data["password"]
            user = authenticate(username, password)

            if not user:
                raise Exception("User not found!")

            access_token = jwt.jwt_encode_callback(user)
            resp = jsonify({"message": "User authenticated", "access_token": access_token.decode("utf-8")})
            resp.status_code = 200
            # add token to response headers - so SwaggerUI can use it
            resp.headers.extend({'jwt-token': access_token})
        except Exception as e:
            print(e)
            resp = jsonify({"message": "Bad username and/or password"})
            resp.status_code = 401

        return resp


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')

api.add_resource(ControlNumber, '/controlnumber/<string:control_number>')
api.add_resource(ControlNumberList, '/controlnumbers')

api.add_resource(Rawmaterial, '/rawmaterial')
api.add_resource(RawmaterialList, '/rawmaterials/<string:control_number>')
api.add_resource(GetRawmaterialsListbyControlNumber, '/getrawbycontrolno/<string:control_number>')

api.add_resource(CarbonNews, '/carbonnews')
api.add_resource(CarbonNewslList, '/carbonnews-lists')
api.add_resource(FindCrabonNewsByHashTag, '/carbonnews/hashtag/<string:hashtag>')
api.add_resource(FindCrabonNewsByTitle, '/carbonnews/title/<string:title>')

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/user/login')
api.add_resource(AddDevice, '/user/add-device')  # for apikey

Swagger(app, config=swagger_config, template=template)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
