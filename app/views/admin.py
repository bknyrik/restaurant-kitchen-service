from flask_admin.contrib import sqla


class DishTypeModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_filters = ("name",)


class IngredientModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_filters = ("name",)


class DishModelView(sqla.ModelView):
    column_list = ("id", "name", "price", "dish_type")


class CookModelView(sqla.ModelView):
    column_list = ("id", "username", "email", "group")
