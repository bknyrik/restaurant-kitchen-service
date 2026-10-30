from flask import Blueprint


blueprint = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)
