from wtforms_alchemy import (
    ModelForm,
    Unique,
    QuerySelectField,
    QuerySelectMultipleField
)
from wtforms import (
    StringField,
    DecimalField,
    TextAreaField,
    validators,
)

from app.database.config import db
from app.database.models import kitchen as models


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
        validators=[validators.DataRequired()]
    )
    description = TextAreaField("Description")
