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

    yield test_app


@pytest.fixture
def test_client(test_app: Flask) -> FlaskClient:
    return test_app.test_client()


@pytest.fixture(scope="module")
def test_group_user(test_app: Flask) -> UserGroupModel:
    with test_app.test_request_context():
        group = UserGroupModel(name=UserGroupEnum.USER)

        db.session.add(group)
        db.session.commit()
        db.session.refresh(group)

        return group


@pytest.fixture(scope="module")
def test_group_moderator(test_app: Flask) -> UserGroupModel:
    with test_app.test_request_context():
        group = UserGroupModel(name=UserGroupEnum.MODERATOR)

        db.session.add(group)
        db.session.commit()
        db.session.refresh(group)

        return group


@pytest.fixture(scope="module")
def test_group_admin(test_app: Flask) -> UserGroupModel:
    with test_app.test_request_context():
        group = UserGroupModel(name=UserGroupEnum.ADMIN)

        db.session.add(group)
        db.session.commit()
        db.session.refresh(group)

        return group


@pytest.fixture(scope="module")
def test_user(
    test_app: Flask,
    test_group_user: UserGroupModel,
) -> models.CookModel:
    with test_app.app_context():
        user = models.CookModel(
            username="testuser",
            password=(
                bcrypt
                .generate_password_hash("Userpass12345")
                .decode()
            ),
            group=test_group_user
        )

        db.session.add(user)
        db.session.commit()
        db.session.refresh(user, attribute_names=("group",))

        return user


@pytest.fixture(scope="module")
def test_moderator(
    test_app: Flask,
    test_group_moderator: UserGroupModel
) -> models.CookModel:
    with test_app.app_context():
        moderator = models.CookModel(
            username="testmoderator",
            password=(
                bcrypt
                .generate_password_hash("Usermoder12345")
                .decode()
            ),
            group=test_group_moderator
        )

        db.session.add(moderator)
        db.session.commit()
        db.session.refresh(moderator, attribute_names=("group",))

        return moderator


@pytest.fixture(scope="module")
def test_admin(
    test_app: Flask,
    test_group_admin: UserGroupModel
) -> models.CookModel:
    with test_app.app_context():
        admin = models.CookModel(
            username="testadmin",
            password=(
                bcrypt
                .generate_password_hash("Useradmin12345")
                .decode()
            ),
            group=test_group_admin
        )

        db.session.add(admin)
        db.session.commit()
        db.session.refresh(admin, attribute_names=("group",))

        return admin


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
