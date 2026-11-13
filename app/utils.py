from flask import Flask

from app import extensions, cli
from app.blueprints import kitchen, accounts
from app.views import error_handlers


def register_extensions(app: Flask) -> None:
    extensions.db.init_app(app)
    extensions.migrate.init_app(app)
    extensions.csrf.init_app(app)
    extensions.login_manager.init_app(app)
    extensions.bcrypt.init_app(app)


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(kitchen.blueprint)
    app.register_blueprint(accounts.blueprint)


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(404, error_handlers.page_not_found_404)
    app.register_error_handler(403, error_handlers.forbidden_403)


def register_cli_commands(app: Flask) -> None:
    app.cli.add_command(cli.create_admin)
    app.cli.add_command(cli.change_password)
