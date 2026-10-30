from flask import View, Response, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt

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
                return redirect(url_for("index"))


        return render_template(self.template, form=form)
