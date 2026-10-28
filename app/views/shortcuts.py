from flask import render_template, redirect, url_for, request, Response
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
