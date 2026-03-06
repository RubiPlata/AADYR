from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt
from controllers.authControllers import auth_bp
from flasgger import Swagger
from flask_cors import CORS

# 👇 IMPORTAMOS SETTINGS
from utils.Key import Settings


def create_app():
    app = Flask(__name__)

    # =========================
    # CARGAR CONFIG BASE
    # =========================
    config = Config()
    app.config.from_object(config)

    # =========================
    # 🔐 INTENTAR CARGAR SECRET DESDE SETTINGS
    # =========================
    settings = Settings()

    try:
        jwt_secret = settings.get("JWT_SECRET_KEY")
        if jwt_secret:
            app.config["JWT_SECRET_KEY"] = jwt_secret
    except Exception:
        # Si no hay AWS o variable, no rompe nada
        pass

    # =========================
    # CORS
    # =========================
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # =========================
    # SWAGGER
    # =========================
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "info": {
            "title": "API Auth Flask",
            "description": "Documentación de API con Swagger y soporte JSON/YAML",
            "version": "1.0.0"
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # =========================
    # EXTENSIONS
    # =========================
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # =========================
    # BLUEPRINTS
    # =========================
    app.register_blueprint(auth_bp, url_prefix="/api")

    # =========================
    # RUTA BASE
    # =========================
    @app.route("/")
    def home():
        return {"message": "API funcionando correctamente"}

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)