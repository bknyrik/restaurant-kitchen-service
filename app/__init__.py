from flask import Flask
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

from app.settings import settings
from app.templatetags import filters
from app.views import error_handlers as eh


def create_app(*, testing: bool = False) -> Flask:
    from app.extensions import csrf, login_manager, bcrypt, db, migrate

    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        settings.SQLALCHEMY_DATABASE_URI if not testing
        else settings.SQLALCHEMY_TEST_DATABASE_URI
    )

    from app.commands import create_admin

    app.cli.add_command(create_admin, "create_admin")

    if testing:
        app.config["WTF_CSRF_ENABLED"] = False

    app.jinja_env.filters["query_transform"] = filters.query_transform

    db.init_app(app)
    migrate.init_app(app)

    csrf.init_app(app)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.database.models import kitchen as models
    from app.database.models.users import UserGroupModel

    from app.views import admin as admin_views

    admin = Admin(
        name="Restaurant Kitchen",
        theme=Bootstrap4Theme(swatch="superhero"),
    )
    admin.init_app(app, index_view=admin_views.HomeAdminView())

    admin.add_view(
        admin_views.DishTypeModelView(
            name="Dish type",
            model=models.DishTypeModel,
            session=db.session,
            url="dish_type"
        )
    )
    admin.add_view(
        admin_views.IngredientModelView(
            name="Ingredient",
            model=models.IngredientModel,
            session=db.session,
            url="ingredient"
        )
    )
    admin.add_view(
        admin_views.DishModelView(
            name="Dish",
            model=models.DishModel,
            session=db.session,
            url="dish"
        )
    )
    admin.add_view(
        admin_views.CookModelView(
            name="Cook",
            model=models.CookModel,
            session=db.session,
            url="cook"
        )
    )
    admin.add_view(
        admin_views.UserGroupModelView(
            name="User group",
            model=UserGroupModel,
            session=db.session,
            url="user_group"
        )
    )

    from app.blueprints import kitchen, accounts

    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)

    app.register_error_handler(404, eh.page_not_found_404)
    app.register_error_handler(403, eh.forbidden_403)
    return app
