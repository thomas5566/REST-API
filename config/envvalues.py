import os

ENV = 'development'
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', 'postgresql://postgres:11880755@flask-database.cueejxouzwxr.ap-northeast-1.rds.amazonaws.com:5432/flasksql')
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
