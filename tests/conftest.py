import os
import sys

# ✅ 添加項目根目錄到 Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ["FLASK_ENV"] = "testing"

import pytest
from flask_jwt_extended import create_access_token

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
            User(
                name="Alice",
                email="alice@example.com",
            ),
            User(
                name="Bob",
                email="bob@example.com",
            ),
        ]

        users[0].set_password("password123")
        users[1].set_password("password123")
        db.session.add_all(users)
        db.session.commit()

        yield [u.id for u in users]

        # 清理(雖然 app fixture 會 drop_all,但這樣更明確)
        db.session.rollback()


@pytest.fixture
def auth_token(app, sample_users):
    """產生測試用的 JWT token"""
    with app.app_context():
        # 因為 identity 使用的是使用者 ID是int型態，所以轉成字串
        token = create_access_token(identity=str(sample_users[0]))
        return token


@pytest.fixture
def auth_headers(auth_token):
    """建立認證 headers"""
    return {"Authorization": f"Bearer {auth_token}"}
