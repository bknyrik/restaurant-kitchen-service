from flask import Flask
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from app.database.config import db, SQLALCHEMY_DATABASE_URI
from app.blueprints import kitchen, accounts
from app.settings import settings
from app.views.accounts import login_manager, bcrypt


csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    bcrypt.init_app(app)


    migrate = Migrate(app, db, directory="app/database/migrations")

    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)
    return app
