import typing

from flask import redirect, url_for, abort, flash
from flask.typing import ResponseReturnValue
from flask_login import current_user
from flask_admin.contrib import sqla
from flask_admin.babel import gettext
from wtforms import Form

from app.database.models import kitchen as models
from app.forms import kitchen as forms
from app.authentication import bcrypt


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
    column_sortable_list = (
        "id",
        "username",
        "email",
        ("group", "group.name")
    )
    column_filters = ("username", "email", "group")

    def create_model(self, form: Form) -> bool | typing.Any:
        session = self.session
        try:
            model = self.build_new_instance()

            form.populate_obj(model)

            model.password = (
                bcrypt.generate_password_hash(form.data["password"])
                .decode()
            )

            session.add(model)
            self._on_model_change(form, model, True)
            session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(
                    gettext("Failed to create record. %(error)s", error=str(ex)),
                    "error",
                )
                sqla.view.log.exception("Failed to create record.")

            session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model

    def update_model(self, form: Form, model: models.CookModel) -> bool:
        session = self.session
        try:
            form.populate_obj(model)

            if form.data["new_password"]:
                model.password = (
                    bcrypt.generate_password_hash(form.data["new_password"])
                    .decode()
                )

            self._on_model_change(form, model, False)
            session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(
                    gettext("Failed to update record. %(error)s", error=str(ex)),
                    "error",
                )
                sqla.view.log.exception("Failed to update record.")

            session.rollback()

            return False
        else:
            self.after_model_change(form, model, False)

        return True

    def get_create_form(self) -> type[Form]:
        return forms.CookAdminCreateForm

    def get_edit_form(self) -> type[Form]:
        return forms.CookAdminUpdateForm
