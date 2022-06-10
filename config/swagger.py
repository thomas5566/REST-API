template = {
    "swagger": "2.0",
    "info": {
        "title": "Rawmaterials API",
        "description": "API for Rawmaterials",
        "contact": {
            "YC Holdings Inc.": "",
            "YC Holdings Developer": "",
            "email": "service@yourcarbon.com.tw",
            "url": "https://aspnex.com/",
        },
        "termsOfService": "https://aspnex.com/",
        "version": "1.0"
    },
    "produces": [
        "application/json",
    ],
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "security": {
        "Authorization": []
    },
    "securitySchemes": {
        "bearerAuth": {
            "bearerFormat": "JWT",
            "scheme": "bearer",
            "type": "http"
        }
    },
    "securityDefinitions": {
        "Authorization": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger-doc"
}
