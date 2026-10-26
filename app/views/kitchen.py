from flask import render_template
from flask.views import View
from sqlalchemy import select

from app.database.config import db
from app.database.models import kitchen as models


class DishTypeListView(View):

    def __init__(self, model: type[models.Base], template: str) -> None:
        self.model = model
        self.template = template

    def dispatch_request(self) -> str:
        dish_types = db.session.execute(
            select(self.model)
            .order_by(self.model.name)
        ).scalars().all()

        return render_template(self.template, dish_types=dish_types)
