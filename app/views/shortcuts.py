from flask import render_template, redirect, url_for, request, Response
from flask.views import View
from flask_wtf import Form
from sqlalchemy import select, insert
from flask_sqlalchemy.model import Model

from app.database.config import db


class ListView(View):
    model: type[Model]
    template: str

    def get_object_list(self) -> list[Model]:
        return list(
            db.session.execute(select(self.model)).scalars().all()
        )

    def dispatch_request(self) -> str:
        object_list = self.get_object_list()
        return render_template(self.template, object_list=object_list)


class DetailView(View):
    model: type[Model]
    template: str

    def get_object(self, id: int) -> db.Model:
        return db.get_or_404(self.model, id)

    def dispatch_request(self, id: int) -> str:
        object_ = self.get_object(id)
        return render_template(self.template, object=object_)


class CreateView(View):
    methods = ("GET", "POST")
    model: type[Model]
    template: str
    success_url_name: str
    form_class: type[Form]

    def dispatch_request(self) -> str | Response:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            db.session.execute(insert(self.model).values(**form.data))
            db.session.commit()

            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form)


class UpdateView(View):
    methods = ("GET", "POST")
    model: type[Model]
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
    model: type[Model]
    template: str
    success_url_name: str

    def dispatch_request(self, id: int) -> str | Response:
        object_ = db.get_or_404(self.model, id)

        if request.method == "POST":
            db.session.delete(object_)
            db.session.commit()
            return redirect(url_for(self.success_url_name))

        return render_template(self.template, object=object_)
