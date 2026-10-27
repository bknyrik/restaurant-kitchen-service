from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms import StringField, validators
from sqlalchemy import select

from app.database.config import db
from app.database.models import kitchen as models


class DishTypeForm(ModelForm, FlaskForm):

    class Meta:
        model = models.DishTypeModel

    name = StringField("Name", [validators.Length(min=4),])

    def validate_name(self, name: StringField) -> None:
        dish_type = db.session.execute(
            select(self.model)
            .where(self.model.name == name.data)
        ).scalar_one_or_none()

        if dish_type:
            raise validators.ValidationError(
                "Dish type with this name already exists."
            )
