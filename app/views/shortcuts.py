from flask import render_template
from flask.views import View
from sqlalchemy import select

from app.database.config import db
from app.database.models.base import Base


class ListView(View):
    model: type[Base]
    template: str

    def dispatch_request(self) -> str:
        object_list = db.session.execute(
            select(self.model)
        ).scalars().all()
        return render_template(self.template, object_list=object_list)
