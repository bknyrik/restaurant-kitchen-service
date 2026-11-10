import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db


@pytest.fixture(scope="module")
def test_app():
    test_app = create_app(testing=True)

    with test_app.app_context():
        db.create_all()

    yield test_app


@pytest.fixture
def test_client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()
