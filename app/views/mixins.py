from flask import abort
from flask_sqlalchemy.model import Model
from flask_login import login_required

from app.extensions import db


class LoginRequiredMixin:

    @login_required
    def dispatch_request(self, *args, **kwargs):
        return super().dispatch_request(*args, **kwargs)


class PermissionRequiredMixin:

    def has_permissions(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def dispatch_request(self, *args, **kwargs):
        if not self.has_permissions(*args, **kwargs):
            abort(403)

        return super().dispatch_request(*args, **kwargs)


class DetailMixin:
    model: type[Model]

    def get_object(self, id_: int) -> Model:
        return db.get_or_404(self.model, id_)
