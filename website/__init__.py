from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'sdffadffadywtefwefyv'

    from .main import main as main_blueprint
    from .auth import auth 

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth, url_prefix='/')

    return app
