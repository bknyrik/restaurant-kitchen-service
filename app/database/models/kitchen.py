from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    DECIMAL,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database.models.base import Base
from app.database.models.users import AbstractUserModel


DishIngredientsModel = Table(
    "dish_ingredients",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("dish_id", ForeignKey("dishes.id"), nullable=False),
    Column("ingredient_id", ForeignKey("ingredients.id"), nullable=False)
)

CookDishesModel = Table(
    "cook_dishes",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("cook_id", ForeignKey("cooks.id"), nullable=False),
    Column("dish_id", ForeignKey("dishes.id"), nullable=False)
)


class DishTypeModel(Base):
    __tablename__ = "dish_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)


class IngredientModel(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)


class DishModel(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=True)
    name = Column(String(255), unique=True, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    dish_type_id = Column(
        Integer,
        ForeignKey("dish_types.id", ondelete="CASCADE"),
        nullable=False
    )
    dish_type = relationship(
        DishTypeModel,
        cascade="all, delete",
        backref="dishes"
    )
    ingredients = relationship(
        IngredientModel,
        secondary=DishIngredientsModel,
        backref="dishes"
    )


class CookModel(AbstractUserModel):
    __tablename__ = "cooks"

    years_of_experience = Column(Integer, nullable=True)
