import os
import pytest
from flask_jwt_extended import create_access_token

os.environ["FLASK_ENV"] = "testing"

from run import create_app
from app import db
from app.models.user_model import User


@pytest.fixture(scope="function")
def app():
    """建立測試用的 Flask app"""
    app = create_app("testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """建立測試用的 Flask client"""
    return app.test_client()


@pytest.fixture
def sample_users(app):
    """建立測試用的假資料"""
    with app.app_context():
        users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com"),
        ]
        users[0].set_password("password123")
        users[1].set_password("password123")

        db.session.add_all(users)
        db.session.commit()

        yield [u.id for u in users]


@pytest.fixture
def auth_token(app, sample_users):
    """產生測試用的 JWT token"""
    with app.app_context():
        token = create_access_token(identity=sample_users[0])
        return token
