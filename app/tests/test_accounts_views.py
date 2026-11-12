import pytest
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


def test_change_password_view(
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        data = {
            "old_password": "Userpass12345",
            "new_password": "NewPass1234",
            "confirm_password": "NewPass1234",
        }
        test_client.post(
            path=url_for("accounts.login"),
            data={
                "username": test_user.username,
                "password": data["old_password"]
            }
        )
        response = test_client.post(
            path=url_for("accounts.change_password"),
            data=data,
            follow_redirects=True
        )

        user = models.CookModel.query.get(ident=test_user.id)

        assert response.status_code == 200
        assert len(response.history) == 1
        assert bcrypt.check_password_hash(user.password, data["new_password"])


@pytest.mark.parametrize(
    "data,error_message,count_messages",
    (
        pytest.param(
            {},
            "This field is required.",
            3,
            id=(
                "Fields old_password, new_password "
                "and confirm_password are required"
            )
        ),
        pytest.param(
            {
                "old_password": "notoldpassword",
                "new_password": "Newpass12345",
                "confirm_password": "Newpass12345"
            },
            "Incorrect password",
            1,
            id="Old password is incorrect"
        ),
        pytest.param(
            {
                "old_password": "Userpass12345",
                "new_password": "notpass",
                "confirm_password": "notpass"
            },
            (
                "Password must have 8 characters and more, "
                "one upper case letter, one lower case letter and "
                "4 digits and more."
            ),
            1,
            id="New password is not matching regex pattern"
        ),
        pytest.param(
            {
                "old_password": "Userpass12345",
                "new_password": "NewPass1234",
                "confirm_password": "newpass1234"
            },
            "The passwords are not matching",
            1,
            id="New password and confirm password are not matching"
        ),
    )
)
def test_change_password_view_invalid_data(
    data: dict,
    error_message: str,
    count_messages: int,
    test_app: Flask,
    test_client: FlaskClient,
    test_user: models.CookModel
) -> None:
    with test_app.test_request_context():
        test_client.post(
            path=url_for("accounts.login"),
            data={
                "username": test_user.username,
                "password": "Userpass12345"
            }
        )
        response = test_client.post(
            path=url_for("accounts.change_password"),
            data=data
        )

        assert response.status_code == 200
        assert error_message in response.get_data(as_text=True)
        assert response.get_data(as_text=True).count(error_message) == count_messages
