import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db
from app.database.models.users import UserGroupModel, UserGroupEnum


@pytest.fixture(scope="module")
def test_app():
    test_app = create_app(testing=True)

    with test_app.app_context():
        db.create_all()
        db.session.execute(
            db.insert(UserGroupModel),
            tuple(
                {"name": group} for group in UserGroupEnum
            )
        )
        db.session.commit()
        db.session.close()

    yield test_app


@pytest.fixture
def test_client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()
