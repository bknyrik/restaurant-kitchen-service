from flask import Flask

from app import extensions
from app.blueprints import kitchen, accounts


def register_extensions(app: Flask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
    extensions.csrf.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.bcrypt.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)
