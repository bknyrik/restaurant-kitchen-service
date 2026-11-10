import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db, bcrypt
from app.database.models.kitchen import CookModel
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


@pytest.fixture
def test_user(test_app: Flask) -> CookModel:
    with test_app.app_context():
        group = UserGroupModel.query.filter_by(
            name=UserGroupEnum.USER
        ).first()

        result = db.session.execute(
            db.insert(CookModel)
            .values(
                username="testuser",
                password=(
                    bcrypt
                    .generate_password_hash("testuser12345")
                    .decode()
                ),
                group=group
            )
            .returning(CookModel)
        )
        db.session.commit()

        user = result.scalars().one()

        db.session.close()

    return user
