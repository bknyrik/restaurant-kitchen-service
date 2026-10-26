from flask import Blueprint

from app.views import kitchen as views
from app.database.models import kitchen as models


blueprint = Blueprint("kitchen", __name__)

blueprint.add_url_rule(
    "/dish_types/",
    view_func=views.DishTypeListView.as_view(
        "dish_type_list",
        models.DishTypeModel,
        "kitchen/dish_type_list.html"
    )
)
