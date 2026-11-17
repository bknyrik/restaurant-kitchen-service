from flask import Flask

from app.utils import application as app_utils


def create_app(*, config: str = "app.settings.DevelopmentConfig") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    app_utils.register_extensions(app)
    app_utils.register_blueprints(app)
    app_utils.register_error_handlers(app)
    app_utils.register_cli_commands(app)
    app_utils.register_jinja_filters(app)
    return app
