from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from app.database.models import kitchen as models


login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id: str) -> models.CookModel:
    return models.CookModel.query.get(int(user_id))
