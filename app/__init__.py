from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from app.blueprints import kitchen, accounts
from app.settings import settings
from app.templatetags import filters
from app.views import error_handlers as eh
from app.views import admin as admin_views


db = SQLAlchemy()
csrf = CSRFProtect()
admin = Admin(
    name="Restaurant Kitchen",
    theme=Bootstrap4Theme(swatch="superhero"),
    index_view=admin_views.HomeAdminView()
)
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app(testing: bool = False) -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        settings.SQLALCHEMY_DATABASE_URI
        if not testing else settings.TEST_DATABASE_URI
    )

    app.jinja_env.filters["query_transform"] = filters.query_transform

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "accounts.login"
    bcrypt.init_app(app)

    from app.database.models import kitchen as models

    @login_manager.user_loader
    def load_user(user_id: str) -> models.CookModel:
        return models.CookModel.query.get(int(user_id))

    admin.init_app(app)

    migrate = Migrate(app, db, directory="app/database/migrations")

    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)

    app.register_error_handler(404, eh.page_not_found_404)
    app.register_error_handler(403, eh.forbidden_403)
    return app
