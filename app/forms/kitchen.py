from wtforms_alchemy import (
    Form,
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

from app.extensions import db, bcrypt
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel, UserGroupEnum
from app.forms import mixins


class DishTypeSearchForm(mixins.SearchByNameMixin, Form):
    ...


class IngredientSearchForm(mixins.SearchByNameMixin, Form):
    ...


class DishSearchForm(mixins.SearchByNameMixin, Form):
    dish_type = QuerySelectField(
        query_factory=lambda: db.session.query(models.DishTypeModel),
        get_label=lambda dish_type: dish_type.name,
        get_pk=lambda dish_type: int(dish_type.id),
        render_kw={"class": "form-select"},
        allow_blank=True,
        blank_text="Search by dish type",
    )


class CookSearchForm(Form):
    username = StringField(
        render_kw={
            "class": "form-control",
            "placeholder": "Search by username"
        }
    )
    group = QuerySelectField(
        get_pk=lambda group: group.id,
        get_label=lambda group: group.name,
        query_factory=lambda: db.session.query(UserGroupModel),
        allow_blank=True,
        blank_text="Search by group",
        render_kw={"class": "form-select"}
    )


class DishTypeForm(ModelForm):

    class Meta:
        model = models.DishTypeModel

    name = StringField(
        label="Name",
        validators=[
            validators.DataRequired(),
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
            validators.DataRequired(),
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
            validators.NumberRange(min=1, max=100000),
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
            validators.Length(min=5, max=25),
            Unique(models.CookModel.username, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )
    first_name = StringField(
        label="First name",
        validators=[
            validators.Optional(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    last_name = StringField(
        label="Last name",
        validators=[
            validators.Optional(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    email = EmailField(
        label="Email",
        validators=[validators.Optional(), validators.Email()],
        render_kw={"class": "form-control"}
    )
    years_of_experience = IntegerField(
        label="Years of experience",
        validators=[
            validators.Optional(),
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

    def populate_obj(self, obj: models.CookModel) -> None:
        for name, field in self._fields.items():
            if name == "password":
                field.data = bcrypt.generate_password_hash(field.data).decode()

            field.populate_obj(obj, name)

        group = (
            db.session.query(UserGroupModel)
            .filter_by(name=UserGroupEnum.USER)
            .first()
        )
        obj.group_id = group.id


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
            validators.Length(min=5, max=25),
            Unique(models.CookModel.username, get_session=lambda: db.session)
        ],
        render_kw={"class": "form-control"}
    )
    first_name = StringField(
        label="First name",
        validators=[
            validators.Optional(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    last_name = StringField(
        label="Last name",
        validators=[
            validators.Optional(),
            validators.Length(min=2, max=20),
        ],
        render_kw={"class": "form-control"}
    )
    email = EmailField(
        label="Email",
        validators=[validators.Optional(), validators.Email()],
        render_kw={"class": "form-control"}
    )
    years_of_experience = IntegerField(
        label="Years of experience",
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ],
        render_kw={"class": "form-control"}
    )


class CookAdminCreateForm(CookCreateForm):
    group = QuerySelectField(
        label="Group",
        get_pk=lambda item: item.id,
        query_factory=lambda: db.session.query(UserGroupModel),
        render_kw={"class": "form-select"},
    )

    def populate_obj(self, obj: models.CookModel) -> None:
        super().populate_obj(obj)
        self.group.populate_obj(obj, "group")


class CookAdminUpdateForm(CookUpdateForm):
    new_password = PasswordField(
        label="New password",
        validators=[
            validators.Optional(),
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

    def populate_obj(self, obj: models.CookModel) -> None:
        for name, field in self._fields.items():
            if name == "new_password" and field.data:
                obj.password = (
                    bcrypt.generate_password_hash(field.data)
                    .decode()
                )
                continue

            field.populate_obj(obj, name)
