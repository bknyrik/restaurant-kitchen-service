from flask_wtf import Form
from wtforms_alchemy import ModelForm
from wtforms import StringField, PasswordField, validators

from app.database.models.kitchen import CookModel


class LoginForm(Form):
    username = StringField(
        "Username",
        validators=[validators.DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired()]
    )


class RegistrationForm(ModelForm):
    class Meta:
        model = CookModel
        only = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )
