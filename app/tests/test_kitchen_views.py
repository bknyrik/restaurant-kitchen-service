from decimal import Decimal

import pytest

from flask import Flask, url_for
from flask_sqlalchemy.model import Model
from flask_login import login_user
from flask.testing import FlaskClient
from wtforms_alchemy import ModelForm

from app import db, bcrypt
from app.database.models import kitchen as models
from app.forms import kitchen as forms
from app.database.models.users import UserGroupModel
from app.tests.conftest import (
    test_app,
    test_client,
    test_user,
    test_moderator,
    test_admin,
    test_group_user,
    test_dish_type_porridge,
    test_dish_type_salad,
    test_dish_salad_by_korean,
    test_ingredient_cheese
)


@pytest.mark.parametrize(
    "endpoint",
    (
        pytest.param("kitchen.index", id="Home"),
        pytest.param("kitchen.dish_type_list", id="Dish type list"),
        pytest.param("kitchen.dish_type_create", id="Create dish type"),
        pytest.param("kitchen.dish_type_update", id="Update dish type"),
        pytest.param("kitchen.dish_type_delete", id="Delete dish type"),
        pytest.param("kitchen.ingredient_list", id="Ingredient list"),
        pytest.param("kitchen.ingredient_create", id="Create ingredient"),
        pytest.param("kitchen.ingredient_update", id="Update ingredient"),
        pytest.param("kitchen.ingredient_delete", id="Delete ingredient"),
        pytest.param("kitchen.dish_list", id="Dish list"),
        pytest.param("kitchen.dish_detail", id="Dish detail"),
        pytest.param("kitchen.dish_create", id="Create dish"),
        pytest.param("kitchen.dish_update", id="Update dish"),
        pytest.param("kitchen.dish_delete", id="Delete dish"),
        pytest.param("kitchen.cook_list", id="Cook list"),
        pytest.param("kitchen.cook_detail", id="Cook detail"),
        pytest.param("kitchen.cook_create", id="Create cook"),
        pytest.param("kitchen.cook_update", id="Update cook"),
        pytest.param("kitchen.cook_delete", id="Delete cook"),
    )
)
def test_kitchen_view_authorization_required(
    endpoint: str,
    test_app: Flask,
    test_client: FlaskClient
) -> None:
    with test_app.test_request_context():
        if (
            endpoint.endswith("detail")
            or endpoint.endswith("update")
            or endpoint.endswith("delete")
        ):
            response = test_client.get(url_for(endpoint, id=999))
        else:
            response = test_client.get(url_for(endpoint))

        assert response.status_code == 302


@pytest.mark.parametrize(
    "endpoint",
    (
        pytest.param("kitchen.dish_type_create", id="Dish type create"),
        pytest.param("kitchen.dish_type_update", id="Dish type update"),
        pytest.param("kitchen.dish_type_delete", id="Dish type delete"),
        pytest.param("kitchen.ingredient_create", id="Ingredient create"),
        pytest.param("kitchen.ingredient_update", id="Ingredient update"),
        pytest.param("kitchen.ingredient_delete", id="Ingredient delete"),
        pytest.param("kitchen.dish_create", id="Dish create"),
        pytest.param("kitchen.dish_update", id="Dish update"),
        pytest.param("kitchen.dish_delete", id="Dish delete"),
        pytest.param("kitchen.cook_create", id="Cook create"),
        pytest.param("kitchen.cook_update", id="Cook update"),
        pytest.param("kitchen.cook_delete", id="Cook delete"),
    )
)
def test_kitchen_view_user_is_forbidden(
    endpoint: str,
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        if not endpoint.endswith("create"):
            response = test_client.get(url_for(endpoint, id=999))
        else:
            response = test_client.get(url_for(endpoint))

        assert response.status_code == 403


@pytest.mark.parametrize(
    "endpoint",
    (
        pytest.param("kitchen.dish_type_delete", id="Dish type delete"),
        pytest.param("kitchen.ingredient_delete", id="Ingredient delete"),
        pytest.param("kitchen.dish_delete", id="Dish delete"),
        pytest.param("kitchen.cook_delete", id="Cook delete"),
    )
)
def test_kitchen_delete_view_moderator_is_forbidden(
    endpoint: str,
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)
        response = test_client.get(url_for(endpoint, id=999))

        assert response.status_code == 403


def test_index_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.get(url_for("kitchen.index"))

        assert response.status_code == 200
        assert "<title>Home</title>" in response.get_data(as_text=True)
        assert test_user.username in response.get_data(as_text=True)


@pytest.mark.parametrize(
    "endpoint,model,title,data",
    (
        pytest.param(
            "kitchen.dish_type_list",
            models.DishTypeModel,
            "Dish types",
            {"name": "Test dish type"},
            id="Dish type list"
        ),
        pytest.param(
            "kitchen.ingredient_list",
            models.IngredientModel,
            "Ingredients",
            {"name": "Test ingredient"},
            id="Ingredient list"
        ),
        pytest.param(
            "kitchen.dish_list",
            models.DishModel,
            "Dishes",
            {"name": "Test dish", "price": Decimal("9.99")},
            id="Dish list"
        ),
        pytest.param(
            "kitchen.cook_list",
            models.CookModel,
            "Cooks",
            {"username": "testcook", "password": "Userpass1234"},
            id="Cook list"
        ),
    )
)
def test_kitchen_list_view(
    endpoint: str,
    model: type[Model],
    title: str,
    data: dict,
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel,
    test_group_user: UserGroupModel,
    test_dish_type_salad: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        match model:
            case models.CookModel:
                data["password"] = (
                    bcrypt
                    .generate_password_hash(data["password"])
                    .decode()
                )
                data["group"] = test_group_user
            case models.DishModel:
                data["dish_type"] = test_dish_type_salad

        instance = model(**data)

        db.session.add(instance)
        db.session.commit()
        db.session.refresh(instance)

        instance_name: str = (
            instance.username
            if isinstance(instance, models.CookModel)
            else instance.name
        )

        response = test_client.get(url_for(endpoint))

        assert response.status_code == 200
        assert f"<title>{title}</title>" in response.get_data(as_text=True)
        assert instance_name in response.get_data(as_text=True)
        assert str(instance.id) in response.get_data(as_text=True)


@pytest.mark.parametrize(
    "endpoint,model,form_class",
    (
        pytest.param(
            "kitchen.dish_type_list",
            models.DishTypeModel,
            forms.DishTypeForm,
            id="Dish type list"
        ),
        pytest.param(
            "kitchen.ingredient_list",
            models.IngredientModel,
            forms.IngredientForm,
            id="Ingredient list"
        ),
        pytest.param(
            "kitchen.dish_list",
            models.DishModel,
            forms.DishForm,
            id="Dish list"
        ),
        pytest.param(
            "kitchen.cook_list",
            models.CookModel,
            forms.CookCreateForm,
            id="Cook list"
        )
    )
)
def test_kitchen_list_view_with_pagination(
    endpoint: str,
    model: type[Model],
    form_class: type[ModelForm],
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_dish_type_porridge: models.DishTypeModel,
    test_group_user: UserGroupModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        data = {}

        match model:
            case models.DishModel:
                data["price"] = Decimal("1.11")
                data["dish_type_id"] = test_dish_type_porridge.id
            case models.CookModel:
                data["password"] = "Moderpass1234"
                data["group_id"] = test_group_user.id

        db.session.bulk_insert_mappings(
            model,
            tuple(
                data | (
                    {"name": f"Test object {number}"}
                    if model is not models.CookModel
                    else {"username": f"testuser{number}"}
                )
                for number in range(12)
            )
        )
        db.session.commit()

        instances = model.query.paginate(per_page=10)
        response = test_client.get(url_for(endpoint))

        assert response.status_code == 200
        assert all(
            inst.name
            if not isinstance(inst, models.CookModel) else inst.username
            in response.get_data(as_text=True) for inst in instances
        )

        query_string = {"page": 2}
        instances = model.query.paginate(**query_string, per_page=10)
        response = test_client.get(
            path=url_for(endpoint),
            query_string=query_string
        )

        assert all(
            inst.name
            if not isinstance(inst, models.CookModel) else inst.username
            in response.get_data(as_text=True) for inst in instances
        )


@pytest.mark.parametrize(
    "endpoint,title",
    (
        pytest.param("kitchen.dish_detail","Dish", id="Dish detail"),
        pytest.param("kitchen.cook_detail", "Cook", id="Cook detail")
    )
)
def test_kitchen_detail_view(
    endpoint: str,
    title: str,
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_dish_salad_by_korean: models.DishModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        match title:
            case "Cook":
                instance = test_user
                instance_name = instance.username
            case "Dish":
                instance = test_dish_salad_by_korean
                instance_name = instance.name

        response = test_client.get(url_for(endpoint, id=instance.id))

        assert response.status_code == 200
        assert f"<title>{title} {instance_name}</title>" in response.get_data(as_text=True)
        assert instance_name in response.get_data(as_text=True)


def test_dish_detail_view_add_cook_to_dish(
    test_app: Flask,
    test_client: FlaskClient,
    test_dish_salad_by_korean: models.DishModel,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.post(
            url_for(
                endpoint="kitchen.dish_detail",
                id=test_dish_salad_by_korean.id
            ),
            follow_redirects=True
        )

        test_dish_salad_by_korean = (
            models.DishModel.query
            .options(db.joinedload(models.DishModel.cooks))
            .get(test_dish_salad_by_korean.id)
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.get_data(as_text=True).count(test_user.username) == 2
        assert test_user in test_dish_salad_by_korean.cooks


def test_dish_detail_view_delete_cook_from_dish(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_dish_salad_by_korean: models.DishModel,
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        test_client.post(
            path=url_for(
                endpoint="kitchen.dish_detail",
                id=test_dish_salad_by_korean.id
            )
        )
        response = test_client.post(
            path=url_for(
                endpoint="kitchen.dish_detail",
                id=test_dish_salad_by_korean.id
            ),
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.get_data(as_text=True).count(test_user.username) == 1


@pytest.mark.parametrize(
    "endpoint,model,data",
    (
        pytest.param(
            "kitchen.dish_type_create",
            models.DishTypeModel,
            {"name": "Casserole"},
            id="Dish type create"
        ),
        pytest.param(
            "kitchen.ingredient_create",
            models.IngredientModel,
            {"name": "Basil"},
            id="Ingredient create"
        ),
        pytest.param(
            "kitchen.dish_create",
            models.DishModel,
            {
                "name": "Semolina porridge",
                "price": Decimal("9.99")
            },
            id="Dish create"
        ),
        pytest.param(
            "kitchen.cook_create",
            models.CookModel,
            {
                "username": "testuser",
                "password": "Userpass1234"
            },
            id="Cook create"
        )
    )
)
def test_kitchen_moderator_create_view(
    endpoint: str,
    model: type[Model],
    data: dict,
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel,
    test_group_user: UserGroupModel,
    test_dish_type_porridge: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        if model is models.DishModel:
            data["dish_type"] = test_dish_type_porridge.id

        response = test_client.post(
            path=url_for(endpoint),
            data=data,
            follow_redirects=True
        )

        match model:
            case models.CookModel:
                data.pop("password")
            case models.DishModel:
                data.pop("dish_type")

        instance = model.query.filter_by(**data).first()

        assert response.status_code == 200
        assert len(response.history) == 1
        assert instance in model.query.all()


def test_kitchen_admin_cook_create_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_group_user: UserGroupModel,
    test_group_moderator: UserGroupModel,
    test_admin: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_admin)

        data = {
            "username": "testmoder",
            "password": "Moderpass1234",
            "group": test_group_moderator.id
        }

        response = test_client.post(
            path=url_for("kitchen.cook_create"),
            data=data,
            follow_redirects=True
        )

        data["group_id"] = data.pop("group")
        password = data.pop("password")

        instance = models.CookModel.query.filter_by(**data).first()

        assert response.status_code == 200
        assert len(response.history) == 1
        assert instance in models.CookModel.query.all()
        assert bcrypt.check_password_hash(instance.password, password)


@pytest.mark.parametrize(
    "endpoint,model,form_class,data",
    (
        pytest.param(
            "kitchen.dish_type_update",
            models.DishTypeModel,
            forms.DishTypeForm,
            {"name": "Pasta"},
            id="Dish type update"
        ),
        pytest.param(
            "kitchen.ingredient_update",
            models.IngredientModel,
            forms.IngredientForm,
            {"name": "Tomato"},
            id="Ingredient update"
        ),
        pytest.param(
            "kitchen.dish_update",
            models.DishModel,
            forms.DishForm,
            {"name": "Ovcharska salata", "price": Decimal("10.15")},
            id="Dish update"
        ),
        pytest.param(
            "kitchen.cook_update",
            models.CookModel,
            forms.CookUpdateForm,
            {"username": "test_user", "years_of_experience": 5},
            id="Cook update"
        )
    )
)
def test_kitchen_moderator_update_view(
    endpoint: str,
    model: type[Model],
    form_class: type[ModelForm],
    data: dict,
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_moderator: models.CookModel,
    test_dish_type_porridge: models.DishTypeModel,
    test_ingredient_cheese: models.IngredientModel,
    test_dish_salad_by_korean: models.DishModel,
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        match model:
            case models.DishTypeModel:
                instance = test_dish_type_porridge
            case models.IngredientModel:
                instance = test_ingredient_cheese
            case models.DishModel:
                instance = test_dish_salad_by_korean
                data["dish_type"] = test_dish_type_porridge.id
            case models.CookModel:
                instance = test_user

        response = test_client.post(
            path=url_for(endpoint, id=instance.id),
            data=data,
            follow_redirects=True
        )

        updated_instance = model.query.get(ident=instance.id)

        input_form_data = form_class(data=data).data
        obj_form_data = form_class(obj=updated_instance).data

        if model is models.DishModel:
            obj_form_data["dish_type"] = obj_form_data["dish_type"].id

        assert response.status_code == 200
        assert len(response.history) == 1
        assert obj_form_data == input_form_data


def test_kitchen_admin_cook_update_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_group_moderator: UserGroupModel,
    test_user: models.CookModel,
    test_admin: models.CookModel,
) -> None:
    with test_app.test_request_context():
        login_user(test_admin)

        data = {
            "username": test_user.username,
            "first_name": "Moderator",
            "new_password": "Moderpass12345",
            "years_of_experience": 3,
            "group": test_group_moderator.id
        }

        response = test_client.post(
            path=url_for("kitchen.cook_update", id=test_user.id),
            data=data,
            follow_redirects=True
        )

        updated_user = models.CookModel.query.get(ident=test_user.id)
        obj_form_data = forms.CookAdminCreateForm(obj=updated_user).data

        data["group"] = obj_form_data["group"] = test_group_moderator.id
        input_form_data = forms.CookAdminUpdateForm(data=data).data

        hashed_password, new_password = (
            obj_form_data.pop("password"),
            input_form_data.pop("new_password")
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert obj_form_data == input_form_data
        assert bcrypt.check_password_hash(hashed_password, new_password)


@pytest.mark.parametrize(
    "endpoint,model",
    (
        pytest.param(
            "kitchen.dish_type_delete",
            models.DishTypeModel,
            id="Dish type delete"
        ),
        pytest.param(
            "kitchen.ingredient_delete",
            models.IngredientModel,
            id="Ingredient delete"
        ),
        pytest.param(
            "kitchen.dish_delete",
            models.DishModel,
            id="Dish delete"
        ),
        pytest.param(
            "kitchen.cook_delete",
            models.CookModel,
            id="Cook delete"
        ),
    )
)
def test_kitchen_admin_delete_view(
    endpoint: str,
    model: type[Model],
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_admin: models.CookModel,
    test_dish_type_salad: models.DishTypeModel,
    test_dish_salad_by_korean: models.DishModel,
    test_ingredient_cheese: models.IngredientModel
) -> None:
    with test_app.test_request_context():
        login_user(test_admin)

        match model:
            case models.DishTypeModel:
                instance = test_dish_type_salad
            case models.IngredientModel:
                instance = test_ingredient_cheese
            case models.DishModel:
                instance = test_dish_salad_by_korean
            case models.CookModel:
                instance = test_user

        response = test_client.post(
            path=url_for(endpoint, id=instance.id),
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert instance not in model.query.all()
