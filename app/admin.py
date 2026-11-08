from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme


admin = Admin(
    name="Restaurant Kitchen",
    theme=Bootstrap4Theme(swatch="darkly")
)
