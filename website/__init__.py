from flask import Flask

from .views import views
from .auth import auth
from .services import login_manager
from .database import init, models

DB_NAME = 'database.db'


@login_manager.user_loader
def load_user(id):
    return models.find_user_by_id(id)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jsfdsdjfsaj'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    init.init()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # with app.app_context():
    #     db.create_all()

    return app
