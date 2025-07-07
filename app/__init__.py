from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


from celery import Celery


swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: **'Bearer &lt;JWT&gt;'**"
        }
    },
    "security": [{"Bearer": []}]
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "🧠 AI Note Summarizer API",
        "description": "Upload PDFs or Text and get smart AI-generated summaries.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: **'Bearer &lt;JWT&gt;'**"
        }
    },
    "security": [{"Bearer": []}]
}


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config.get('CELERY_BROKER_URL'),
        backend=app.config.get('CELERY_RESULT_BACKEND')
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    app = Flask(__name__, static_url_path='/flasgger_static')
    app.config.from_object('instance.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    Swagger(app, config=swagger_config, template=swagger_template)

    from .routes import main
    from .auth.routes import auth

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")

    make_celery(app)

    return app