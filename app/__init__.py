from flask import Flask

from app.settings import settings
from app.templatetags import filters
from app import utils


def create_app(*, testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        settings.SQLALCHEMY_DATABASE_URI if not testing
        else settings.SQLALCHEMY_TEST_DATABASE_URI
    )
    app.config["TESTING"] = testing

    if testing:
        app.config["WTF_CSRF_ENABLED"] = False

    utils.register_extensions(app)
    utils.register_blueprints(app)
    utils.register_error_handlers(app)
    utils.register_cli_commands(app)
    utils.register_jinja_filters(app)
    return app
