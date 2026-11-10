from flask import Flask, url_for
from flask_login import login_user
from flask.testing import FlaskClient

from app.database.models import kitchen as models
from app.tests.conftest import (
    test_app,
    test_client,
    test_user,
    test_dish_type
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
        assert b"<title>Home</title>" in response.data
        assert test_user.username.encode() in response.data


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
    test_dish_type: models.DishTypeModel
) -> None:
    with test_app.test_request_context():
        login_user(test_user)

        response = test_client.get(url_for("kitchen.dish_type_list"))

        assert response.status_code == 200
        assert test_dish_type.name in response.get_data(as_text=True)
