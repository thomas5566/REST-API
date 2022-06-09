import os

ENV = 'development'
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', 'postgresql://postgres:5566@localhost/flasksql')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SWAGGER = {
    'title': "Rawmaterials-API",
    'uiversion': 3,
    "ui_params": {
        "apisSorter": "alpha",
        "operationsSorter": "alpha",
        "tagsSorter": "alpha",
    }
}
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_AUTH_HEADER_NAME = 'Authorization'
JWT_AUTH_HEADER_PREFIX = 'Bearer'
