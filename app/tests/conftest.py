import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app, db, bcrypt
from app.database.models import kitchen as models
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

    yield test_app


@pytest.fixture
def test_client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()


@pytest.fixture(scope="module")
def test_user(test_app: Flask) -> models.CookModel:
    with test_app.app_context():
        group = UserGroupModel.query.filter_by(
            name=UserGroupEnum.USER
        ).first()

        user = models.CookModel(
            username="testuser",
            password=(
                bcrypt
                .generate_password_hash("Userpass12345")
                .decode()
            ),
            group=group
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user, attribute_names=("group",))

        return user


@pytest.fixture(scope="module")
def test_dish_type_porridge(test_app: Flask) -> models.DishTypeModel:
    with test_app.app_context():
        dish_type = models.DishTypeModel(name="Porridge")

        db.session.add(dish_type)
        db.session.commit()
        db.session.refresh(dish_type)

        return dish_type


@pytest.fixture(scope="module")
def test_dish_type_salad(test_app: Flask) -> models.DishTypeModel:
    with test_app.app_context():
        dish_type = models.DishTypeModel(name="Salad")

        db.session.add(dish_type)
        db.session.commit()
        db.session.refresh(dish_type)

        return dish_type
