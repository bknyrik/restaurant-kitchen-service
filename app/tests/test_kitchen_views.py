from flask import Flask, url_for
from flask_login import login_user
from flask.testing import FlaskClient

from app.database.models import kitchen as models
from app.tests.conftest import (
    test_app,
    test_client,
    test_user,
    test_dish_type_porridge,
    test_dish_type_salad
)


def test_index_view_authorization_required(
    test_app: Flask,
    test_client: FlaskClient
) -> None:
    with test_app.test_request_context():
        response = test_client.get(url_for("kitchen.index"))

        assert response.status_code != 200


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


def test_dish_type_list_view_authorization_required(
    test_app: Flask,
    test_client: FlaskClient
) -> None:
    with test_app.test_request_context():
        response = test_client.get(url_for("kitchen.dish_type_list"))

        assert response.status_code != 200


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


def test_dish_type_create_view_is_forbidden(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel,
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.post(url_for("kitchen.dish_type_create"))
        assert response.status_code == 403, response.data
