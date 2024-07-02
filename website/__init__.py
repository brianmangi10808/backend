from flask import Flask
from flask_session import Session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from .config import ApplicationConfig
from .models import db

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ApplicationConfig)

    bcrypt.init_app(app)
    CORS(app, supports_credentials=True)
    server_session = Session(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
