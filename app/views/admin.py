import typing

from flask import redirect, url_for, abort
from flask.typing import ResponseReturnValue
from flask_login import current_user
from flask_admin import AdminIndexView
from flask_admin.contrib import sqla
from wtforms import Form

from app.forms import kitchen as forms


class AdminView(sqla.ModelView):
    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.group.name ==  "admin"
        )

    def inaccessible_callback(
        self,
        name: typing.Any,
        **kwargs: typing.Any
    ) -> ResponseReturnValue:
        if (
            current_user.is_authenticated
            and current_user.group.name != "admin"
        ):
            abort(403)

        return redirect(url_for("accounts.login"))


class HomeAdminView(AdminIndexView):
    def is_accessible(self) -> bool:
        return (
            current_user.is_authenticated
            and current_user.group.name ==  "admin"
        )

    def inaccessible_callback(
        self,
        name: typing.Any,
        **kwargs: typing.Any
    ) -> ResponseReturnValue:
        if (
            current_user.is_authenticated
            and current_user.group.name != "admin"
        ):
            abort(403)

        return redirect(url_for("accounts.login"))


class DishTypeModelView(AdminView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.DishTypeForm


class IngredientModelView(AdminView):
    column_list = ("id", "name")
    column_sortable_list = ("id", "name")
    column_filters = ("name",)
    form = forms.IngredientForm


class DishModelView(AdminView):
    column_list = ("id", "name", "price", "dish_type")
    can_view_details = True
    column_details_list = (
        "id",
        "name",
        "price",
        "description",
        "dish_type",
        "ingredients",
        "cooks"
    )
    column_sortable_list = (
        "id",
        "name",
        "price",
        ("dish_type", "dish_type.name")
    )
    column_filters = ("name", "price", "dish_type")
    form = forms.DishForm


class CookModelView(AdminView):
    column_list = ("id", "username", "email", "group")
    can_view_details = True
    column_details_list = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "created_at",
        "updated_at",
        "group"
    )
    column_sortable_list = (
        "id",
        "username",
        "email",
        ("group", "group.name")
    )
    column_filters = ("username", "email", "group")

    def get_create_form(self) -> type[Form]:
        return forms.CookAdminCreateForm

    def get_edit_form(self) -> type[Form]:
        return forms.CookAdminUpdateForm


class UserGroupModelView(sqla.ModelView):
    column_display_pk = True
    can_delete = False
