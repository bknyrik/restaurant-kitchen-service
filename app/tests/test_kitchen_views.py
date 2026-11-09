from flask import Flask, url_for
from flask.testing import FlaskClient

from app.tests.conftest import test_app, test_client


def test_index_view_authorization_required(
    test_app: Flask,
    test_client: FlaskClient
) -> None:
    with test_app.test_request_context():
        response = test_client.get(url_for("kitchen.index"))

        assert response.status_code != 200
