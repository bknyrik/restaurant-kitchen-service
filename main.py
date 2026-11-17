from app import create_app


gunicorn_app = create_app(config="app.settings.ProductionConfig")
