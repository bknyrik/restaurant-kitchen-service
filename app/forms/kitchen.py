from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms import StringField, validators

from app.database.config import db
from app.database.models import kitchen as models


class DishTypeForm(ModelForm, FlaskForm):

    class Meta:
        model = models.DishTypeModel

    name = StringField("Name", [validators.Length(min=4),])
