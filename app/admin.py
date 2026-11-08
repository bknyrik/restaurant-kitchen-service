from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

from app.database.config import db
from app.views import admin as views
from app.database.models import kitchen as models


admin = Admin(
    name="Restaurant Kitchen",
    theme=Bootstrap4Theme(swatch="darkly")
)
admin.add_view(
    views.DishTypeModelView(
        name="Dish type",
        model=models.DishTypeModel,
        session=db.session
    )
)
