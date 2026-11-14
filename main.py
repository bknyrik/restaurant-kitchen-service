from app import create_app


if __name__ == "__main__":
    app = create_app()
else:
    gunicorn_app = create_app(config="app.settings.ProductionConfig")
