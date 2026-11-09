import pytest

from app import create_app, db


@pytest.fixture
def test_app():
    test_app = create_app(testing=True)

    with test_app.app_context():
        db.create_all()

    yield test_app
