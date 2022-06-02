import os

ENV = 'development'
DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:5566@localhost/flasksql'
SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL', 'postgresql://postgres:5566@localhost/flasksql')
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SWAGGER = {'title': "Rawmaterials-API", 'uiversion': 3}

# uri = os.getenv("DATABASE_URL")  # or other relevant config var
# if uri.startswith("postgres://"):
#     uri = uri.replace("postgres://", "postgresql://", 1)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(uri, 'sqlite:///data.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:5566@localhost/flasksql'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['SWAGGER'] = {'title': "Rawmaterials-API", 'uiversion': 3}
