from wtforms_alchemy import ModelForm, Unique
from wtforms import StringField, validators

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
