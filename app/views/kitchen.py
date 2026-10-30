from app.database.models import kitchen as models
from app.forms import kitchen as forms
from app.views import shortcuts, mixins


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
    model = models.DishModel
    template = "kitchen/dish_detail.html"


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
