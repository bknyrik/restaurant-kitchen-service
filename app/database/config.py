from flask_sqlalchemy import SQLAlchemy

from app.settings import settings
from app.database.models.base import Base


SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

db = SQLAlchemy(model_class=Base)
