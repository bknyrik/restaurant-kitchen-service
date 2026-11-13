from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from app.database.models.kitchen import CookModel


csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "accounts.login"
bcrypt = Bcrypt()
db = SQLAlchemy()


@login_manager.user_loader
def load_user(user_id: str) -> CookModel:
    return CookModel.query.get(int(user_id))
