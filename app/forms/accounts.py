from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from flask_login import current_user
from flask_bcrypt import check_password_hash

from app.forms.kitchen import (
    CookCreateForm,
    PASSWORD_REGEX_PATTERN,
    PASSWORD_REGEX_ERROR_MESSAGE
)


class LoginForm(Form):
    username = StringField(
        "Username",
        validators=[validators.DataRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[validators.DataRequired()]
    )


class SignupForm(CookCreateForm):

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

    old_password = PasswordField(
        label="Old password",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"}
    )
    new_password = PasswordField(
        label="New password",
        validators=[
            validators.DataRequired(),
            validators.Regexp(
                regex=PASSWORD_REGEX_PATTERN,
                message=PASSWORD_REGEX_ERROR_MESSAGE
            )
        ],
        render_kw={"class": "form-control"}
    )
    confirm_password = PasswordField(
        label="Confirm new password",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"}
    )

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
