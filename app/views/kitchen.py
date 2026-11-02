from flask import request, Response, render_template, redirect, url_for
from flask_login import current_user, login_required
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


class DishTypeCreateView(mixins.LoginRequiredMixin, shortcuts.CreateView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"


class DishTypeUpdateView(mixins.LoginRequiredMixin, shortcuts.UpdateView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"


class DishTypeDeleteView(mixins.LoginRequiredMixin, shortcuts.DeleteView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_delete_form.html"
    success_url_name = "kitchen.dish_type_list"


class IngredientListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.IngredientModel
    template = "kitchen/ingredient_list.html"


class IngredientCreateView(mixins.LoginRequiredMixin, shortcuts.CreateView):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"


class IngredientUpdateView(mixins.LoginRequiredMixin, shortcuts.UpdateView):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"


class IngredientDeleteView(mixins.LoginRequiredMixin, shortcuts.DeleteView):
    model = models.IngredientModel
    template = "kitchen/ingredient_delete_form.html"
    success_url_name = "kitchen.ingredient_list"


class DishListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.DishModel
    template = "kitchen/dish_list.html"


class DishDetailView(mixins.LoginRequiredMixin, shortcuts.DetailView):
    methods = ("GET", "POST")
    model = models.DishModel
    template = "kitchen/dish_detail.html"

    @login_required
    def dispatch_request(self, *args, **kwargs) -> str | Response:
        object_ = self.get_object(kwargs["id"])

        if request.method == "POST":
            if current_user not in object_.cooks:
                object_.cooks.append(current_user)
            else:
                object_.cooks.remove(current_user)

            db.session.commit()
            return redirect(url_for("kitchen.dish_detail", id=object_.id))

        return render_template(self.template, object=object_)


class DishCreateView(mixins.LoginRequiredMixin, shortcuts.CreateView):
    model = models.DishModel
    template = "kitchen/dish_form.html"
    form_class = forms.DishForm
    success_url_name = "kitchen.dish_list"


class DishUpdateView(mixins.LoginRequiredMixin, shortcuts.UpdateView):
    model = models.DishModel
    template = "kitchen/dish_form.html"
    form_class = forms.DishForm
    success_url_name = "kitchen.dish_list"


class DishDeleteView(mixins.LoginRequiredMixin, shortcuts.DeleteView):
    model = models.DishModel
    template = "kitchen/dish_delete_form.html"
    success_url_name = "kitchen.dish_list"


class CookListView(mixins.LoginRequiredMixin, shortcuts.ListView):
    model = models.CookModel
    template = "kitchen/cook_list.html"


class CookDetailView(mixins.LoginRequiredMixin, shortcuts.DetailView):
    model = models.CookModel
    template = "kitchen/cook_detail.html"


class CookCreateView(mixins.LoginRequiredMixin, shortcuts.CreateView):
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


class CookUpdateView(mixins.LoginRequiredMixin, shortcuts.UpdateView):
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


class CookDeleteView(mixins.LoginRequiredMixin, shortcuts.DeleteView):
    model = models.CookModel
    template = "kitchen/cook_delete_form.html"
    success_url_name = "kitchen.cook_list"
