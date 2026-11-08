from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

from app.database.config import db
from app.views import admin as views
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel


admin = Admin(
    name="Restaurant Kitchen",
    theme=Bootstrap4Theme(swatch="superhero")
)
admin.add_view(
    views.DishTypeModelView(
        name="Dish type",
        model=models.DishTypeModel,
        session=db.session
    )
)
admin.add_view(
    views.IngredientModelView(
        name="Ingredient",
        model=models.IngredientModel,
        session=db.session
    )
)
admin.add_view(
    views.DishModelView(
        name="Dish",
        model=models.DishModel,
        session=db.session
    )
)
admin.add_view(
    views.CookModelView(
        name="Cook",
        model=models.CookModel,
        session=db.session,
        url="cook"
    )
)
admin.add_view(
    views.UserGroupModelView(
        name="User group",
        model=UserGroupModel,
        session=db.session,
        url="user_group"
    )
)
