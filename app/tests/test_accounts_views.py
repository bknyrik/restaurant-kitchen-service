from flask import Flask, url_for
from flask.testing import FlaskClient

from app.database.models import kitchen as models
from app.tests.conftest import test_app, test_client, test_user


def test_login_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        response = test_client.post(
            path=url_for("accounts.login"),
            data={
                "username": test_user.username,
                "password": "Userpass12345"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert test_user.username in response.get_data(as_text=True)


def test_login_view_invalid_account_credentials(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        response = test_client.post(
            path=url_for("accounts.login"),
            data={"username": "notuser", "password": "notpassword"},
        )

        assert response.status_code == 200
        assert "<title>Login</title>" in response.get_data(as_text=True)
        assert "Invalid account credentials" in response.get_data(as_text=True)


def test_logout_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        test_client.post(
            path=url_for("accounts.login"),
            data={"username": test_user.username, "password": "Userpass12345"}
        )
        response = test_client.post(
            url_for("accounts.logout"),
            follow_redirects=True
        )

        assert response.status_code == 200
        assert "<title>Login</title>" in response.get_data(as_text=True)
        assert test_user.username not in response.get_data(as_text=True)
