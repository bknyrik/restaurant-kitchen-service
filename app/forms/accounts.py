from flask_wtf import Form
from wtforms_alchemy import ModelForm, Unique
from wtforms import (
    StringField,
    IntegerField,
    EmailField,
    PasswordField,
    validators
)
from flask_login import current_user

from app import db, bcrypt
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel, UserGroupEnum
from app.forms.kitchen import (
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


class SignupForm(ModelForm):
    class Meta:
        model = models.CookModel
        only = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "password",
        )

    username = StringField(
        label="Username",
        validators=[
            validators.DataRequired(),
            validators.Length(min=5, max=25),
            Unique(models.CookModel.username, get_session=lambda: db.session)
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
        validators=[validators.DataRequired(), validators.Email()],
        render_kw={"class": "form-control"}
    )
    years_of_experience = IntegerField(
        label="Years of experience",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1)
        ],
        render_kw={"class": "form-control"}
    )
    password = PasswordField(
        label="Password",
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
        label="Confirm password",
        validators=[validators.DataRequired()],
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

    def populate_obj(self, obj: models.CookModel) -> None:
        for name, field in self._fields.items():
            if name == "password":
                field.data = (
                    bcrypt.generate_password_hash(field.data)
                    .decode()
                )

            field.populate_obj(obj, name)

        obj.group_id = (
            UserGroupModel.query.
            filter_by(name=UserGroupEnum.USER)
            .first().id
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
            not bcrypt.check_password_hash(
                pw_hash=current_user.password,
                password=old_password.data
            )
        ):
            raise validators.ValidationError("Incorrect password")

    def validate_confirm_password(
        self,
        confirm_password: PasswordField
    ) -> None:
        if confirm_password.data != self.new_password.data:
            raise validators.ValidationError("The passwords are not matching")
