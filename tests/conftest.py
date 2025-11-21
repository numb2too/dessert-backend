import os
import pytest

# ⚠️ 必須在 import app 之前設定
os.environ["TESTING"] = "1"

from run import create_app
from app import db
from app.models.user_model import User


@pytest.fixture(scope="function")
def app():
    """建立測試用的 Flask app (每個測試獨立)"""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    app = create_app(config=test_config)

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
        db.session.add_all(users)
        db.session.commit()
