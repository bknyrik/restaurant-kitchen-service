from flask import Blueprint

from app.views import authentication as views


blueprint = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)
blueprint.add_url_rule("/login/", views.LoginView.as_view("login"))
