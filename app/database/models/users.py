from enum import StrEnum, auto

from flask_login import UserMixin

from app.database.config import db


class UserGroupEnum(StrEnum):
    USER = auto()
    MODERATOR = auto()
    ADMIN = auto()


class UserGroupModel(db.Model):
    __tablename__ = "user_groups"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.Enum(UserGroupEnum), unique=True, nullable=False)


class UserGroupMixin:

    @db.declared_attr
    def group_id(cls):
        return db.Column(
            db.Integer,
            db.ForeignKey("user_groups.id", ondelete="CASCADE"),
            nullable=False
        )

    @db.declared_attr
    def group(cls):
        return db.relationship(UserGroupModel)


class AbstractUserModel(UserMixin, UserGroupMixin, db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False
    )

    def get_id(self) -> str:
        return str(self.id)
