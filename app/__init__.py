from flask import Flask

from app.settings import settings
from app.templatetags import filters
from app.views import error_handlers as eh
from app.extensions import csrf, login_manager, bcrypt, db, migrate
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel
from app.views import admin as admin_views
from app.blueprints import kitchen, accounts
from app import cli


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

    app.jinja_env.filters["query_transform"] = filters.query_transform

    db.init_app(app)
    migrate.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)

    app.register_error_handler(404, eh.page_not_found_404)
    app.register_error_handler(403, eh.forbidden_403)

    app.cli.add_command(cli.create_admin)
    app.cli.add_command(cli.change_password)
    return app
