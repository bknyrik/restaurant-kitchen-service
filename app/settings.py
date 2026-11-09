import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}"
        f"@{os.getenv("DB_HOST")}:"
        f"{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}"
    )
    TEST_DATABASE_URI = "sqlite://"
    SECRET_KEY = os.getenv("SECRET_KEY")


settings = Settings()
