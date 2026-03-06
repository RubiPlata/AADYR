from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()


# =========================
# SWAGGER TEMPLATE
# =========================
swagger_template = {
    "openapi": "3.0.0",
    "info": {
        "title": "API",
        "description": "API del 83",
        "version": "1.0"
    },
    "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Ambiente Local"
        }
    ],
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ]
}