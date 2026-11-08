from flask_admin.contrib import sqla

from app.forms import kitchen as forms


class DishTypeModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.DishTypeForm


class IngredientModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.IngredientForm


class DishModelView(sqla.ModelView):
    column_list = ("id", "name", "price", "dish_type")
    column_sortable_list = ("id", "name", "price", "dish_type")
    column_filters = ("name", "price", "dish_type")
    form = forms.DishForm


class CookModelView(sqla.ModelView):
    column_list = ("id", "username", "email", "group")
    column_sortable_list = (
        "id",
        "username",
        "email",
        ("group", "group.name")
    )
    column_filters = ("username", "email", "group")
