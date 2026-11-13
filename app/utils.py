from flask import Flask

from app import extensions, cli
from app.blueprints import kitchen, accounts
from app.views import error_handlers, admin as admin_views
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel


def register_extensions(app: Flask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
    extensions.csrf.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.bcrypt.init_app(app)
    extensions.admin.init_app(
        app,
        index_view=admin_views.HomeAdminView()
    )

    @extensions.login_manager.user_loader
    def load_user(user_id: str) -> models.CookModel:
        return models.CookModel.query.get(int(user_id))


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(404, error_handlers.page_not_found_404)
    app.register_error_handler(403, error_handlers.forbidden_403)


def register_cli_commands(app: Flask) -> None:
    app.cli.add_command(cli.create_admin)
    app.cli.add_command(cli.change_password)


def register_admin_views() -> None:
    extensions.admin.add_view(
        admin_views.DishTypeModelView(
            name="Dish type",
            model=models.DishTypeModel,
            session=extensions.db.session,
            url="dish_type"
        )
    )
    extensions.admin.add_view(
        admin_views.IngredientModelView(
            name="Ingredient",
            model=models.IngredientModel,
            session=extensions.db.session,
            url="ingredient"
        )
    )
    extensions.admin.add_view(
        admin_views.DishModelView(
            name="Dish",
            model=models.DishModel,
            session=extensions.db.session,
            url="dish"
        )
    )
    extensions.admin.add_view(
        admin_views.CookModelView(
            name="Cook",
            model=models.CookModel,
            session=extensions.db.session,
            url="cook"
        )
    )
    extensions.admin.add_view(
        admin_views.UserGroupModelView(
            name="User group",
            model=UserGroupModel,
            session=extensions.db.session,
            url="user_group"
        )
    )
