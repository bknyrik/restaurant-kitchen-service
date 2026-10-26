from flask import Flask
from flask_migrate import Migrate

from app.database.config import db


def create_app() -> Flask:
    app = Flask(__name__)

    db.init_app(app)

    migrate = Migrate(app, db, directory="app/database/migrations")

    return app
