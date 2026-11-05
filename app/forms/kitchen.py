from wtforms_alchemy import (
    ModelForm,
    Unique,
    QuerySelectField,
    QuerySelectMultipleField
)
from wtforms import (
    StringField,
    PasswordField,
    EmailField,
    IntegerField,
    DecimalField,
    TextAreaField,
    validators,
)

from app.database.config import db
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel


class DishTypeForm(ModelForm):

    class Meta:
        model = models.DishTypeModel

    name = StringField(
        label="Name",
        validators=[
            validators.Length(min=4, max=25),
            Unique(models.DishTypeModel.name, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )


class IngredientForm(ModelForm):

    class Meta:
        model = models.IngredientModel

    name = StringField(
        label="Name",
        validators=[
            validators.Length(min=4, max=25),
            Unique(models.IngredientModel.name, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )


class DishForm(ModelForm):

    class Meta:
        model = models.DishModel

    name = StringField(
        label="Name",
        validators=[
            validators.DataRequired(),
            validators.Length(min=5, max=50),
            Unique(models.DishModel.name, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )
    dish_type = QuerySelectField(
        "Dish type",
        query_factory=lambda: db.session.query(models.DishTypeModel),
        get_label=lambda dish_type: dish_type.name,
        get_pk=lambda dish_type: int(dish_type.id),
        render_kw={"class": "form-select"}
    )
    ingredients = QuerySelectMultipleField(
        label="Ingredients",
        query_factory=lambda: db.session.query(models.IngredientModel),
        get_label=lambda ingredient: ingredient.name,
        get_pk=lambda ingredient: int(ingredient.id),
        render_kw={"class": "form-select"}
    )
    price = DecimalField(
        "Price",
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1)
        ],
        render_kw={"class": "form-control"}
    )
    description = TextAreaField(
        "Description",
        render_kw={"class": "form-control"}
    )
    cooks = QuerySelectMultipleField(
        label="Cooks",
        query_factory=lambda: db.session.query(models.CookModel),
        get_label=lambda cook: cook.username,
        get_pk=lambda cook: cook.id,
        render_kw={"class": "form-select"}
    )


PASSWORD_REGEX_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=(.*\d){4,}).{8,}$"
PASSWORD_REGEX_ERROR_MESSAGE = (
    "Password must have 8 characters and more, "
    "one upper case letter, one lower case letter and 4 digits and more."
)


class CookCreateForm(ModelForm):
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
            validators.Length(min=6, max=25),
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
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=25),
        ],
        render_kw={"class": "form-control"}
    )
    years_of_experience = IntegerField(
        label="Years of experience",
        validators=[validators.NumberRange(min=1)],
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


class CookUpdateForm(ModelForm):
    class Meta:
        model = models.CookModel
        only = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience"
        )

    username = StringField(
        label="Username",
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=25),
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
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=25),
        ],
        render_kw={"class": "form-control"}
    )
    years_of_experience = IntegerField(
        label="Years of experience",
        validators=[validators.NumberRange(min=1)],
        render_kw={"class": "form-control"}
    )


class CookAdminCreateForm(CookCreateForm):
    group = QuerySelectField(
        label="Group",
        get_pk=lambda item: item.id,
        query_factory=lambda: db.session.query(UserGroupModel),
        render_kw={"class": "form-select"},
    )


class CookAdminUpdateForm(CookUpdateForm):
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
    group = QuerySelectField(
        label="Group",
        get_pk=lambda item: item.id,
        query_factory=lambda: db.session.query(UserGroupModel),
        render_kw={"class": "form-select"},
    )
