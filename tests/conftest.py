import os
import pytest

# 設定測試環境（必須在 import app 之前）
os.environ["FLASK_ENV"] = "testing"

from run import create_app
from app import db
from app.models.user_model import User


@pytest.fixture(scope="function")
def app():
    """建立測試用的 Flask app (每個測試獨立)"""
    app = create_app("testing")

    # 可覆蓋特定配置（如使用記憶體資料庫）
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
        db.session.add_all(users)
        db.session.commit()

        # 回傳 user ids 供測試使用
        yield [u.id for u in users]
