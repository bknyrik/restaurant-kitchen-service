from flask.views import View
from flask import Response, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt

from app.database.config import db
from app.database.models import kitchen as models
from app.forms import authentication as forms


login_manager = LoginManager()
bcrypt = Bcrypt()


@login_manager.user_loader
def load_user(user_id: str) -> models.CookModel:
    return models.CookModel.query.get(int(user_id))


class LoginView(View):
    methods = ("GET", "POST")
    template = "authentication/login.html"

    def dispatch_request(self) -> str | Response:
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
                    "authentication/login.html",
                    error="Invalid account credentials",
                    form=form
                )


        return render_template(self.template, form=form)


class LogoutView(View):

    @login_required
    def dispatch_request(self) -> Response:
        logout_user()
        return redirect(url_for("auth.login"))


class SignupView(View):
    methods = ("GET", "POST")
    template = "authentication/signup.html"
    model = models.CookModel
    form_class = forms.RegistrationForm
    success_url_name = "kitchen.index"

    def dispatch_request(self) -> str | Response:
        form = self.form_class(request.form)

        if request.method == "POST" and form.validate():
            object_ = self.model()
            form.populate_obj(object_)
            db.session.commit()
            login_user(object_)
            return redirect(url_for(self.success_url_name))

        return render_template(self.template, form=form)
