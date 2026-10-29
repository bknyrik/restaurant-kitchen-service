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


class DishTypeUpdateView(shortcuts.UpdateView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_form.html"
    form_class = forms.DishTypeForm
    success_url_name = "kitchen.dish_type_list"


class DishTypeDeleteView(shortcuts.DeleteView):
    model = models.DishTypeModel
    template = "kitchen/dish_type_delete_form.html"
    success_url_name = "kitchen.dish_type_list"


class IngredientListView(shortcuts.ListView):
    model = models.IngredientModel
    template = "kitchen/ingredient_list.html"


class IngredientCreateView(shortcuts.CreateView):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"


class IngredientUpdateView(shortcuts.UpdateView):
    model = models.IngredientModel
    template = "kitchen/ingredient_form.html"
    form_class = forms.IngredientForm
    success_url_name = "kitchen.ingredient_list"


class IngredientDeleteView(shortcuts.DeleteView):
    model = models.IngredientModel
    template = "kitchen/ingredient_delete_form.html"
    success_url_name = "kitchen.ingredient_list"


class DishListView(shortcuts.ListView):
    model = models.DishModel
    template = "kitchen/dish_list.html"


class DishDetailView(shortcuts.DetailView):
    model = models.DishModel
    template = "kitchen/dish_detail.html"


class DishDeleteView(shortcuts.DeleteView):
    model = models.DishModel
    template = "kitchen/dish_delete_form.html"
    success_url_name = "kitchen.dish_list"
