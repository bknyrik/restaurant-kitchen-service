from flask import Flask, url_for
from flask.testing import FlaskClient

from app import bcrypt
from app.database.models import kitchen as models
from app.database.models.users import UserGroupModel
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


def test_logout_view_authorization_required(
    test_app: Flask,
    test_client: FlaskClient,
) -> None:
    with test_app.test_request_context():
        response = test_client.post(
            path=url_for("accounts.logout"),
            follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert "<title>Login</title>" in response.get_data(as_text=True)


def test_signup_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_group_user: UserGroupModel
) -> None:
    with test_app.test_request_context():
        data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@gmail.com",
            "password": "Userpass1234",
            "confirm_password": "Userpass1234",
            "years_of_experience": 5
        }

        response = test_client.post(
            path=url_for("accounts.signup"),
            data=data,
            follow_redirects=True
        )

        raw_password = data.pop("password")
        del data["confirm_password"]

        user = models.CookModel.query.filter_by(**data).first()

        assert response.status_code == 200
        assert "<title>Home</title>" in response.get_data(as_text=True)
        assert user.username in response.get_data(as_text=True)
        assert bcrypt.check_password_hash(user.password, raw_password)
