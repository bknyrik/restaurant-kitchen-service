from flask.views import View
from flask.typing import ResponseReturnValue
from flask import request, redirect, render_template, url_for
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app.extensions import db, bcrypt
from app.database.models import kitchen as models
from app.forms import accounts as forms
from app.views import shortcuts


class LoginView(View):
    methods = ("GET", "POST")
    template = "accounts/login.html"

    def dispatch_request(self) -> ResponseReturnValue:
        form = forms.LoginForm(request.form)

        if request.method == "POST" and form.validate():
            username, password = (
                form.data["username"],
                form.data["password"]
            )

            cook: models.CookModel | None = (
                models.CookModel.query
                .filter(models.CookModel.username == username)
                .first()
            )

            if cook and bcrypt.check_password_hash(cook.password, password):
                login_user(cook)
                return redirect(url_for("kitchen.index"))
            else:
                return render_template(
                    "accounts/login.html",
                    error="Invalid account credentials",
                    form=form
                )


        return render_template(self.template, form=form)


class LogoutView(View):
    methods = ("POST",)

    @login_required
    def dispatch_request(self) -> ResponseReturnValue:
        logout_user()
        return redirect(url_for("accounts.login"))


class SignupView(shortcuts.CreateView):
    template = "accounts/signup.html"
    model = models.CookModel
    form_class = forms.SignupForm
    success_url_name = "kitchen.index"

    def dispatch_request(self) -> ResponseReturnValue:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            object_ = self.model()
            form.populate_obj(object_)

            db.session.add(object_)
            db.session.commit()
            db.session.refresh(object_)

            login_user(object_)
            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form)


class ChangePasswordView(View):
    methods = ("GET", "POST")
    form_class = forms.ChangePasswordForm
    template = "accounts/change_password.html"

    @login_required
    def dispatch_request(self) -> ResponseReturnValue:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            current_user.password = (
                bcrypt.generate_password_hash(form.data["new_password"])
                .decode()
            )

            db.session.commit()
            return redirect(
                url_for("kitchen.cook_detail", id=current_user.id)
            )

        return render_template(self.template, form=form)
