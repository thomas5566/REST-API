from flask_restful import Resource, reqparse
from models.user import UserModel

from flask_restful_swagger_2 import Resource, swagger

class UserRegister(Resource):
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

    @swagger.doc({
        'tags': ['User Register'],
        'description': 'Adds a User',
        'reqparser': {'name': 'User Register',
                      'parser': parser},
        'responses': {
            '201': {
                'description': 'Created User',
                'examples': {
                    'application/json': {
                        "username": "thomas",
                        "password": "5566"
                    }
                }
            }
        }
    })
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201
