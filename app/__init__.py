from flask import Flask
from flask_migrate import Migrate

from app.database.config import db, SQLALCHEMY_DATABASE_URI
from app.blueprints import kitchen


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    migrate = Migrate(app, db, directory="app/database/migrations")

    app.register_blueprint(kitchen.blueprint)
    return app
