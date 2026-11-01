from flask_sqlalchemy.model import Model
from flask_login import login_required

from app.database.config import db


class LoginRequiredMixin:

    @login_required
    def dispatch_request(self, *args, **kwargs):
        return super().dispatch_request(*args, **kwargs)


class DetailMixin:
    model: type[Model]

    def get_object(self, id_: int) -> Model:
        return db.get_or_404(self.model, id_)
