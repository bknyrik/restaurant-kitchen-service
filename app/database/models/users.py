from enum import StrEnum, auto

from sqlalchemy import (
    Column,
    Integer,
    Enum,
    String,
    ForeignKey
)
from sqlalchemy.orm import (
    relationship,
    declarative_mixin,
    declared_attr,
)

from app.database.models.base import Base


class UserGroupEnum(StrEnum):
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()


class UserGroupModel(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserGroupEnum), unique=True, nullable=False)


@declarative_mixin
class AbstractUserModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)
    group_id = Column(
        Integer,
        ForeignKey("user_groups.id", ondelete="CASCADE"),
        nullable=False
    )

    @declared_attr
    def group(cls):
        return relationship(
            UserGroupModel,
            cascade="all, delete",
            uselist=False
        )
