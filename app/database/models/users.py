from enum import StrEnum, auto

from sqlalchemy import Column, Integer, Enum

from app.database.models.base import Base


class UserGroupEnum(StrEnum):
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()


class UserGroupModel(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserGroupEnum), unique=True, nullable=False)
