from flask import render_template, redirect, url_for, request, Response
from flask.views import View
from flask_wtf import Form
from flask_sqlalchemy.model import Model

from app.database.config import db
from app.views import mixins


class TemplateView(View):
    template: str

    def get_context_data(self) -> dict:
        return dict()

    def dispatch_request(self) -> str:
        return render_template(self.template, **self.get_context_data())


class ListView(View):
    model: type[Model]
    template: str

    def get_object_list(self) -> list[Model]:
        return self.model.query.all()

    def dispatch_request(self) -> str:
        object_list = self.get_object_list()
        return render_template(self.template, object_list=object_list)


class DetailView(mixins.DetailMixin, View):
    model: type[Model]
    template: str

    def dispatch_request(self, id: int) -> str:
        object_ = self.get_object(id)
        return render_template(self.template, object=object_)


class CreateView(View):
    methods = ("GET", "POST")
    model: type[Model]
    template: str
    success_url_name: str
    form_class: type[Form]

    def get_form_class(self) -> type[Form]:
        return self.form_class

    def dispatch_request(self) -> str | Response:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            object_ = self.model()

            form.populate_obj(object_)

            db.session.add(object_)
            db.session.commit()

            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form)


class UpdateView(View):
    methods = ("GET", "POST")
    model: type[Model]
    template: str
    success_url_name: str
    form_class: type[Form]

    def get_form(self, object_: Model) -> Form:
        form = self.form_class(obj=object_)

        if request.method == "POST":
            form.process(request.form)

        return form

    def dispatch_request(self, id: int) -> str | Response:
        object_ = db.get_or_404(self.model, id)
        form = self.get_form(object_)

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
