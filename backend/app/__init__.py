from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    app.url_map.strict_slashes = False

    from app.auth import auth_bp
    from app.opportunities import opportunities_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(opportunities_bp, url_prefix='/opportunities')

    @app.route("/")
    def home():
        return "Flask Backend Running Successfully"

    return app