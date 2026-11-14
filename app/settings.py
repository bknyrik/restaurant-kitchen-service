import os

from dotenv import load_dotenv


load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv("POSTGRES_USER")}"
        f":{os.getenv("POSTGRES_PASSWORD")}"
        f"@{os.getenv("POSTGRES_HOST")}"
        f":{os.getenv("POSTGRES_PORT")}"
        f"/{os.getenv("POSTGRES_DB")}"
    )
    PREFERRED_URL_SCHEME = "https"


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv("POSTGRES_USER")}"
        f":{os.getenv("POSTGRES_PASSWORD")}"
        f"@{os.getenv("POSTGRES_HOST")}"
        f":{os.getenv("POSTGRES_PORT")}"
        f"/{os.getenv("POSTGRES_DB")}"
    )


class TestConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    WTF_CSRF_ENABLED = False
