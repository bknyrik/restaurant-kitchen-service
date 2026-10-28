from flask import render_template, request, redirect, url_for, Response
from flask.views import View
from sqlalchemy import select, insert

from app.database.config import db
from app.database.models import kitchen as models
from app.forms import kitchen as forms
from app.views import shortcuts


class DishTypeListView(shortcuts.ListView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_list.html"


class DishTypeCreateView(shortcuts.CreateView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"


class DishTypeUpdateView(View):
    methods = ("GET", "POST")
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"

    def dispatch_request(self, id: int) -> str | Response:
        dish_type = db.session.execute(
            select(self.model)
            .where(self.model.id == id)
        ).scalar_one_or_none()

        form = forms.DishTypeForm(request.form, obj=dish_type)

        if request.method == "POST" and form.validate():
            form.populate_obj(dish_type)
            db.session.commit()
            return redirect(url_for("kitchen.dish_type_list"))

        return render_template(self.template, form=form, dish_type=dish_type)


class DishTypeDeleteView(shortcuts.DeleteView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_delete_form.html"
    success_url_name = "kitchen.dish_type_list"


class IngredientListView(shortcuts.ListView):
    model = models.IngredientModel
    template = "kitchen/ingredient_list.html"


class IngredientCreateView(View):
    methods = ("GET", "POST")
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"

    def dispatch_request(self) -> str | Response:
        form = forms.IngredientForm(request.form)

        if request.method == "POST" and form.validate():
            db.session.execute(
                insert(self.model)
                .values(name=form.data["name"])
            )
            db.commit()
            return redirect(url_for("kitchen.ingredient_list"))

        return render_template(self.template, form=form)


class IngredientDeleteView(shortcuts.DeleteView):
    model = models.IngredientModel
    template = "kitchen/ingredient_delete_form.html"
    success_url_name = "kitchen.ingredient_list"
