from flask_admin.contrib import sqla


class DishTypeModelView(sqla.ModelView):
    column_list = ("id", "name")


class IngredientModelView(sqla.ModelView):
    column_list = ("id", "name")
