from flask import Blueprint

from app.views import kitchen as views


blueprint = Blueprint("kitchen", __name__)

blueprint.add_url_rule(
    "/dish_types/",
    view_func=views.DishTypeListView.as_view("dish_type_list")
)
blueprint.add_url_rule(
    "/dish_types/create/",
    view_func=views.DishTypeCreateView.as_view("dish_type_create")
)
blueprint.add_url_rule(
    "/dish_types/<int:id>/update/",
    view_func=views.DishTypeUpdateView.as_view("dish_type_update")
)
blueprint.add_url_rule(
    "/dish_types/<int:id>/delete/",
    view_func=views.DishTypeDeleteView.as_view("dish_type_delete")
)
blueprint.add_url_rule(
    "/ingredients/",
    view_func=views.IngredientListView.as_view("ingredient_list")
)
