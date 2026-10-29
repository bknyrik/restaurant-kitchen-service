from wtforms_alchemy import (
    ModelForm,
    Unique,
    QuerySelectField,
    QuerySelectMultipleField
)
from wtforms import (
    StringField,
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
            validators.Length(min=4),
            Unique(models.DishTypeModel.name, get_session=lambda: db.session)
        ]
    )


class IngredientForm(ModelForm):

    class Meta:
        model = models.IngredientModel

    name = StringField(
        label="Name",
        validators=[
            validators.Length(min=4),
            Unique(models.IngredientModel.name, get_session=lambda: db.session)
        ]
    )


class DishForm(ModelForm):

    class Meta:
        model = models.DishModel

    name = StringField(
        label="Name",
        validators=[
            validators.DataRequired(),
            validators.Length(min=5),
            Unique(models.DishModel.name, get_session=lambda: db.session)
        ]
    )
    dish_type = QuerySelectField(
        "Dish type",
        query_factory=lambda: db.session.query(models.DishTypeModel),
        get_label=lambda dish_type: dish_type.name,
        get_pk=lambda dish_type: int(dish_type.id)
    )
    ingredients = QuerySelectMultipleField(
        label="Ingredients",
        query_factory=lambda: db.session.query(models.IngredientModel),
        get_label=lambda ingredient: ingredient.name,
        get_pk=lambda ingredient: int(ingredient.id)
    )
