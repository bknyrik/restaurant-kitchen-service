import pytest

from flask import Flask, url_for
from flask_login import login_user, logout_user
from flask.testing import FlaskClient

from app.database.models import kitchen as models
from app.tests.conftest import (
    test_app,
    test_client,
    test_user,
    test_moderator,
    test_admin,
    test_dish_type_porridge,
    test_dish_type_salad
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


def test_dish_type_list_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_dish_type_porridge: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.get(url_for("kitchen.dish_type_list"))

        assert response.status_code == 200
        assert "<title>Dish types</title>" in response.get_data(as_text=True)
        assert test_dish_type_porridge.name in response.get_data(as_text=True)


def test_dish_type_list_view_filter_by_name(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_dish_type_porridge: models.DishTypeModel,
    test_dish_type_salad: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.get(
            path=url_for("kitchen.dish_type_list"),
            query_string={"name": "A"}
        )

        assert response.status_code == 200
        assert test_dish_type_porridge.name not in response.get_data(as_text=True)
        assert test_dish_type_salad.name in response.get_data(as_text=True)


def test_dish_type_create_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel,
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        data = {"name": "Soup"}

        response = test_client.post(
            path=url_for("kitchen.dish_type_create"),
            data=data
        )
        dish_type = models.DishTypeModel.query.filter_by(**data).first()

        assert response.status_code == 302
        assert dish_type is not None and dish_type.name == data["name"]


def test_dish_type_create_view_already_exists(
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        data = {"name": "Salad"}
        response = test_client.post(
            path=url_for("kitchen.dish_type_create"),
            data=data
        )

        assert "Already exists." in response.get_data(as_text=True)


def test_dish_type_update_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel,
    test_dish_type_salad: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        data = {"name": "Bread"}
        response = test_client.post(
            path=url_for(
                endpoint="kitchen.dish_type_update",
                id=test_dish_type_salad.id
            ),
            data=data
        )

        dish_type = models.DishTypeModel.query.get(
            ident=test_dish_type_salad.id
        )

        assert response.status_code == 302
        assert dish_type.name == data["name"]


def test_dish_type_update_view_already_exists(
    test_app: Flask,
    test_client: FlaskClient,
    test_moderator: models.CookModel,
    test_dish_type_salad: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_moderator)

        response = test_client.post(
            path=url_for(
                endpoint="kitchen.dish_type_update",
                id=test_dish_type_salad.id
            ),
            data={"name": "Porridge"}
        )

        assert "Already exists." in response.get_data(as_text=True)


def test_dish_type_delete_view_is_forbidden(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
    test_moderator: models.CookModel,
    subtests
) -> None:
    with test_app.test_request_context():
        for user in (test_user, test_moderator):
            with subtests.test(user.group.name.capitalize()):
                login_user(user)
                response = test_client.post(
                    path=url_for(
                        endpoint="kitchen.dish_type_delete",
                        id=999
                    )
                )
                assert response.status_code == 403
                logout_user()


def test_dish_type_delete_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_admin: models.CookModel,
    test_dish_type_salad: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_admin)

        response = test_client.post(
            url_for(
                endpoint="kitchen.dish_type_delete",
                id=test_dish_type_salad.id
            )
        )

        dish_type = models.DishTypeModel.query.get(
            ident=test_dish_type_salad.id
        )

        assert response.status_code == 302
        assert dish_type is None
