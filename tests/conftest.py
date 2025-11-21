import os
import sys
import pytest

# 將專案根目錄加入 Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from run import app
from app import db
from app.models.user_model import User


@pytest.fixture
def client():
    """建立測試用的 Flask client"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def sample_users(client):
    """建立測試用的假資料"""
    with app.app_context():
        user1 = User(name="Alice", email="alice@example.com")
        user2 = User(name="Bob", email="bob@example.com")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
