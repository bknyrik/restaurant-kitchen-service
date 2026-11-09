from flask import request, render_template, redirect, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.pagination import Pagination
from wtforms import Form

from app.database.config import db
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel
from app.forms import kitchen as forms
from app.views import shortcuts, mixins
from app.views.accounts import bcrypt


class IndexView(mixins.LoginRequiredMixin, shortcuts.TemplateView):
    template = "index.html"

    def get_context_data(self) -> dict:
        return {
            "count_dish_types": models.DishTypeModel.query.count(),
            "count_ingredients": models.IngredientModel.query.count(),
            "count_dishes": models.DishModel.query.count(),
            "count_cooks": models.CookModel.query.count(),
        }


class DishTypeListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_list.html"
    paginate_by = 10

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        context["search_form"] = forms.DishTypeSearchForm(request.args)
        return context

    def get_object_list(self) -> list[Model] | Pagination:
        search_form = self.get_context_data()["search_form"]

        query = self.model.query
        name = search_form.name.data

        if name:
            query = query.filter(self.model.name.icontains(name))

        return (
            query.all() if self.paginate_by is None
            else query.paginate(per_page=self.paginate_by)
        )


class DishTypeCreateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.CreateView
):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class DishTypeUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.UpdateView
):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class DishTypeDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.DeleteView
):
    model = models.DishTypeModel
    template = "kitchen/dish_type_delete_form.html"
    success_url_name = "kitchen.dish_type_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name == "admin"


class IngredientListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.IngredientModel
    template = "kitchen/ingredient_list.html"
    paginate_by = 10

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        context["search_form"] = forms.IngredientSearchForm(request.args)
        return context

    def get_object_list(self) -> list[Model] | Pagination:
        search_form = self.get_context_data()["search_form"]

        query = self.model.query
        name = search_form.name.data

        if name:
            query = query.filter(self.model.name.icontains(name))

        return (
            query.all() if self.paginate_by is None
            else query.paginate(per_page=self.paginate_by)
        )


class IngredientCreateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.CreateView
):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class IngredientUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.UpdateView
):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class IngredientDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.DeleteView
):
    model = models.IngredientModel
    template = "kitchen/ingredient_delete_form.html"
    success_url_name = "kitchen.ingredient_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name == "admin"


class DishListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.DishModel
    template = "kitchen/dish_list.html"
    paginate_by = 10

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        context["search_form"] = forms.DishSearchForm(request.args)
        return context

    def get_object_list(self, *args, **kwargs) -> list[Model] | Pagination:
        search_form = self.get_context_data()["search_form"]

        query = self.model.query
        name = search_form.name.data
        dish_type = search_form.dish_type.data

        if name:
            query = query.filter(self.model.name.icontains(name))

        if dish_type is not None:
            query = query.filter(
                self.model.dish_type_id == dish_type.id
            )

        return (
            query.all() if self.paginate_by is None
            else query.paginate(per_page=self.paginate_by)
        )


class DishDetailView(
    mixins.LoginRequiredMixin,
    shortcuts.ListView,
    shortcuts.DetailView
):
    methods = ("GET", "POST")
    model = models.DishModel
    template = "kitchen/dish_detail.html"
    paginate_by = 10

    def get_object_list(
        self,
        *args,
        **kwargs
    ) -> list[Model] | Pagination:
        return (
            models.CookModel
            .query
            .join(models.CookDishesModel)
            .where(models.CookDishesModel.c.dish_id == kwargs["id"])
            .paginate(
                per_page=self.paginate_by
            )
        )

    @login_required
    def dispatch_request(self, *args, **kwargs) -> ResponseReturnValue:
        object_ = self.get_object(kwargs["id"])
        object_list = self.get_object_list(id=kwargs["id"])

        if request.method == "POST":
            if current_user not in object_.cooks:
                object_.cooks.append(current_user)
            else:
                object_.cooks.remove(current_user)

            db.session.commit()
            return redirect(url_for("kitchen.dish_detail", id=object_.id))

        return render_template(
            self.template,
            object=object_,
            object_list=object_list
        )


class DishCreateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.CreateView
):
    model = models.DishModel
    template = "kitchen/dish_form.html"
    form_class = forms.DishForm
    success_url_name = "kitchen.dish_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class DishUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.UpdateView
):
    model = models.DishModel
    template = "kitchen/dish_form.html"
    form_class = forms.DishForm
    success_url_name = "kitchen.dish_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class DishDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.DeleteView
):
    model = models.DishModel
    template = "kitchen/dish_delete_form.html"
    success_url_name = "kitchen.dish_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name == "admin"


class CookListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.CookModel
    template = "kitchen/cook_list.html"
    paginate_by = 10

    def get_context_data(self) -> dict:
        context = super().get_context_data()
        context["search_form"] = forms.CookSearchForm(request.args)
        return context

    def get_object_list(self, *args, **kwargs) -> list[Model] | Pagination:
        search_form = self.get_context_data()["search_form"]

        query = self.model.query
        username = search_form.username.data
        group = search_form.group.data

        if username:
            query = query.filter(self.model.username.icontains(username))

        if group is not None:
            query = query.filter(self.model.group_id == group.id)

        return (
            query.all() if self.paginate_by is None
            else query.paginate(per_page=self.paginate_by)
        )


class CookDetailView(
    mixins.LoginRequiredMixin,
    shortcuts.ListView,
    shortcuts.DetailView
):
    model = models.CookModel
    template = "kitchen/cook_detail.html"
    paginate_by = 10

    def get_object_list(self, *args, **kwargs) -> list[Model] | Pagination:
        return (
            models.DishModel
            .query
            .join(models.CookDishesModel)
            .where(models.CookDishesModel.c.cook_id == kwargs["id"])
            .paginate(
                per_page=self.paginate_by
            )
        )

    @login_required
    def dispatch_request(self, *args, **kwargs) -> ResponseReturnValue:
        object_ = self.get_object(kwargs["id"])
        object_list = self.get_object_list(id=kwargs["id"])

        return render_template(
            self.template,
            object=object_,
            object_list=object_list
        )


class CookCreateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.CreateView
):
    model = models.CookModel
    template = "kitchen/cook_form.html"
    success_url_name = "kitchen.cook_list"

    def get_form_class(
        self
    ) -> type[forms.CookCreateForm | forms.CookAdminCreateForm]:
        if current_user.group.name == "admin":
            return forms.CookAdminCreateForm

        return forms.CookCreateForm

    def create_object(self, form: Form) -> None:
        object_ = self.model()

        form.populate_obj(object_)

        object_.password = (
            bcrypt.generate_password_hash(
                form.data["password"]
            ).decode()
        )

        if current_user.group.name != "admin":
            group = db.session.query(UserGroupModel).filter(
                UserGroupModel.name == "USER"
            ).first()

            object_.group = group

        db.session.add(object_)
        db.session.commit()
        db.session.refresh(object_)

    def has_permissions(self, *args, **kwargs) -> bool:
        return current_user.group.name in ("admin", "moderator")


class CookUpdateView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.UpdateView
):
    model = models.CookModel
    template = "kitchen/cook_form.html"
    success_url_name = "kitchen.cook_list"

    def get_form_class(
        self
    ) -> type[forms.CookUpdateForm | forms.CookAdminCreateForm]:
        if current_user.group.name == "admin":
            return forms.CookAdminUpdateForm

        return forms.CookUpdateForm

    def update_object(self, form: Form, object_: models.CookModel) -> None:
        form.populate_obj(object_)

        if form.data.get("new_password"):
            object_.password = bcrypt.generate_password_hash(
                form.data["new_password"]
            ).decode()

        db.session.commit()

    def has_permissions(self, *args, **kwargs) -> bool:
        return (
            current_user.id == kwargs["id"]
            or current_user.group.name in ("moderator", "admin")
        )


class CookDeleteView(
    mixins.LoginRequiredMixin,
    mixins.PermissionRequiredMixin,
    shortcuts.DeleteView
):
    model = models.CookModel
    template = "kitchen/cook_delete_form.html"
    success_url_name = "kitchen.cook_list"

    def has_permissions(self, *args, **kwargs) -> bool:
        return (
            current_user.id == kwargs["id"]
            or current_user.group.name == "admin"
        )
