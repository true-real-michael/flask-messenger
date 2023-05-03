from flask import Flask
from flask_login import LoginManager

from .views import views
from .auth import auth
from .database import db
from .database import models

login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return db.find_user_by_id(id)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'prikol3000'

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
