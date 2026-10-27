from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm, Unique
from wtforms import StringField, validators

from app.database.config import db
from app.database.models import kitchen as models


class DishTypeForm(ModelForm, FlaskForm):

    class Meta:
        model = models.DishTypeModel

    name = StringField(
        label="Name",
        validators=[
            validators.Length(min=4),
            Unique(models.DishTypeModel.name, get_session=lambda: db.session)
        ]
    )
