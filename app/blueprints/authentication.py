from flask import Blueprint

from app.views import authentication as views


blueprint = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)
blueprint.add_url_rule(
    "/login/",
    view_func=views.LoginView.as_view("login")
)
blueprint.add_url_rule(
    "/logout/",
    view_func=views.LogoutView.as_view("logout")
)
