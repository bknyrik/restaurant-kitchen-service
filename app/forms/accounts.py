from flask_wtf import Form
from wtforms_alchemy import ModelForm, Unique
from wtforms import StringField, PasswordField, EmailField, validators
from flask_login import current_user
from flask_bcrypt import check_password_hash

from app.database.config import db
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


class SignupForm(ModelForm):
    class Meta:
        model = CookModel
        only = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )


    username = StringField(
        label="Username",
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=25),
            Unique(CookModel.username, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )
    first_name = StringField(
        label="First name",
        validators=[
            validators.DataRequired(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    last_name = StringField(
        label="Last name",
        validators=[
            validators.DataRequired(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    email = EmailField(
        label="Email",
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=25),
        ],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        label="Password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=8, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    confirm_password = PasswordField(
        label="Confirm password",
        validators=[
            validators.Length(min=8, max=20)
        ],
        render_kw={"class": "form-control"}
    )

    def validate_confirm_password(
        self,
        confirm_password: PasswordField
    ) -> None:
        if self.password.data != confirm_password.data:
            raise validators.ValidationError(
                "The passwords are not matching"
            )


class ChangePasswordForm(Form):

    old_password = PasswordField("Old password")
    new_password = PasswordField("New password")
    confirm_password = PasswordField("Confirm new password")

    def validate_old_password(self, old_password: PasswordField) -> None:
        if (
            not check_password_hash(
                pw_hash=current_user.password,
                password=old_password.data
            )
        ):
            raise validators.ValidationError("Enter the correct password")

    def validate_confirm_password(
        self,
        confirm_password: PasswordField
    ) -> None:
        if confirm_password.data != self.new_password.data:
            raise validators.ValidationError("The passwords are not matching")
