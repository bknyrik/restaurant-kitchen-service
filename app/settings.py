import os

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}"
        f"@{os.getenv("DB_HOST")}:"
        f"{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
    )


class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
