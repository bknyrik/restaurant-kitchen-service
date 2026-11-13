from app.extensions import db
from app.database.models.users import AbstractUserModel


DishIngredientsModel = db.Table(
    "dish_ingredients",
    db.Model.metadata,
    db.Column(
        "dish_id",
        db.ForeignKey("dishes.id"),
        primary_key=True
    ),
    db.Column(
        "ingredient_id",
        db.ForeignKey("ingredients.id"),
        primary_key=True
    )
)


CookDishesModel = db.Table(
    "cook_dishes",
    db.Model.metadata,
    db.Column("cook_id", db.ForeignKey("cooks.id"), nullable=False),
    db.Column("dish_id", db.ForeignKey("dishes.id"), nullable=False)
)


class DishTypeModel(db.Model):
    __tablename__ = "dish_types"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    dishes = db.relationship(
        "DishModel",
        cascade="all, delete-orphan",
        back_populates="dish_type"
    )

    def __str__(self) -> str:
        return self.name


class IngredientModel(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __str__(self) -> str:
        return self.name


class DishModel(db.Model):
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    dish_type_id = db.Column(
        db.Integer,
        db.ForeignKey("dish_types.id", ondelete="CASCADE"),
        nullable=False
    )
    dish_type = db.relationship(DishTypeModel, back_populates="dishes")
    ingredients = db.relationship(
        IngredientModel,
        secondary=DishIngredientsModel,
        backref="dishes"
    )
    cooks = db.relationship(
        "CookModel",
        secondary=CookDishesModel,
        backref="dishes"
    )


class CookModel(AbstractUserModel):
    __tablename__ = "cooks"

    years_of_experience = db.Column(db.Integer, nullable=True)
