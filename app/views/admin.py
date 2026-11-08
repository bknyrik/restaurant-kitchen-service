import typing

from flask import redirect, url_for, abort
from flask.typing import ResponseReturnValue
from flask_login import current_user
from flask_admin.contrib import sqla

from app.forms import kitchen as forms


class AdminView(sqla.ModelView):
    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.group.name in ("moderator", "admin")
        )

    def inaccessible_callback(
        self,
        name: typing.Any,
        **kwargs: typing.Any
    ) -> ResponseReturnValue:
        if (
            current_user.is_authenticated
            and current_user.group.name not in ("moderator", "admin")
        ):
            abort(403)

        return redirect(url_for("accounts.login"))


class DishTypeModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.DishTypeForm

    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.group.name in ("moderator", "admin")
        )

    def inaccessible_callback(
        self,
        name: typing.Any,
        **kwargs: typing.Any
    ) -> ResponseReturnValue:
        if (
            current_user.is_authenticated
            and current_user.group.name not in ("moderator", "admin")
        ):
            abort(403)

        return redirect(url_for("accounts.login"))


class IngredientModelView(sqla.ModelView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.IngredientForm


class DishModelView(sqla.ModelView):
    column_list = ("id", "name", "price", "dish_type")
    column_sortable_list = (
        "id",
        "name",
        "price",
        ("dish_type", "dish_type.name")
    )
    column_filters = ("name", "price", "dish_type")
    form = forms.DishForm


class CookModelView(sqla.ModelView):
    column_list = ("id", "username", "email", "group")
    column_sortable_list = (
        "id",
        "username",
        "email",
        ("group", "group.name")
    )
    column_filters = ("username", "email", "group")
