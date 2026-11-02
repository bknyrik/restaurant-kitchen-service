from flask import Blueprint

from app.views import accounts as views


blueprint = Blueprint(
    name="accounts",
    import_name=__name__,
    url_prefix="/accounts"
)
blueprint.add_url_rule(
    "/login/",
    view_func=views.LoginView.as_view("login")
)
blueprint.add_url_rule(
    "/logout/",
    view_func=views.LogoutView.as_view("logout")
)
blueprint.add_url_rule(
    "/signup/",
    view_func=views.SignupView.as_view("signup")
)
