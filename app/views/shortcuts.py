from flask import render_template, redirect, url_for, request, Response
from flask.views import View
from flask_wtf import Form
from sqlalchemy import select, insert

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


class DetailView(View):
    model: type[Base]
    template: str

    def dispatch_request(self, id: int) -> str:
        object_ = db.get_or_404(self.model, id)
        return render_template(self.template, object=object_)


class CreateView(View):
    methods = ("GET", "POST")
    model: type[Base]
    template: str
    success_url_name: str
    form_class: type[Form]

    def dispatch_request(self) -> str | Response:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            data = form.data
            data.pop("csrf_token", None)

            db.session.execute(insert(self.model).values(**data))
            db.session.commit()

            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form)


class UpdateView(View):
    methods = ("GET", "POST")
    model: type[Base]
    template: str
    success_url_name: str
    form_class: type[Form]

    def dispatch_request(self, id: int) -> str | Response:
        object_ = db.get_or_404(self.model, id)
        form = self.form_class(request.form, obj=object_)

        if request.method == "POST" and form.validate():
            form.populate_obj(object_)
            db.session.commit()
            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form, object=object_)


class DeleteView(View):
    methods = ("GET", "POST")
    model: type[Base]
    template: str
    success_url_name: str

    def dispatch_request(self, id: int) -> str | Response:
        object_ = db.get_or_404(self.model, id)

        if request.method == "POST":
            db.session.delete(object_)
            db.session.commit()
            return redirect(url_for(self.success_url_name))

        return render_template(self.template, object=object_)
