from flask import Flask
from flask_migrate import Migrate

from app.database.config import db, SQLALCHEMY_DATABASE_URI


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)

    migrate = Migrate(app, db, directory="app/database/migrations")

    return app
