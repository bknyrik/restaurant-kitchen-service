from sqlalchemy import Column, Integer, String

from app.database.models.base import Base


class DishTypeModel(Base):
    __tablename__ = "dish_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
