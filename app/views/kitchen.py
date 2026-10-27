from flask import render_template, request, redirect, url_for, Response
from flask.views import View
from sqlalchemy import select, insert

from app.database.config import db
from app.database.models import kitchen as models
from app.forms import kitchen as forms


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


class DishTypeCreateView(View):
    methods = ("GET", "POST")

    def __init__(self, model: type[models.Base], template: str) -> None:
        self.model = model
        self.template = template

    def dispatch_request(self) -> str | Response:
        form = forms.DishTypeForm(request.form)

        if request.method == "POST" and form.validate():
            db.session.execute(
                insert(self.model)
                .values(**form.data)
            )
            db.session.commit()
            return redirect(url_for("kitchen.dish_type_list"))

        return render_template(self.template, form=form)
