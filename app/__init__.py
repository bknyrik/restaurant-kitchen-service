from flask import Flask

from app import settings
from app import utils


def create_app(
    *,
    config: settings.BaseConfig = settings.DevelopmentConfig()
) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    utils.register_extensions(app)
    utils.register_blueprints(app)
    utils.register_error_handlers(app)
    utils.register_cli_commands(app)
    utils.register_jinja_filters(app)
    return app
