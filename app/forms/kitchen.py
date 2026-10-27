from flask_wtf import FlaskForm
from wtforms import StringField, validators


class DishTypeForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=4),])
