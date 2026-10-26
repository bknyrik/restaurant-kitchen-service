from flask import render_template
from flask.views import View
from sqlalchemy import select

from app.database.config import db
from app.database.models import kitchen as models


class DishTypeListView(View):

    def __init__(self) -> None:
        self.model = models.DishTypeModel
        self.template = "kitchen/dish_type_list.html"

    def dispatch_request(self) -> str:
        dish_types = db.session.execute(
            select(self.model)
            .order_by(self.model.name)
        ).scalars().all()

        return render_template(self.template, dish_types=dish_types)
