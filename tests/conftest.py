import os
import sys
import pytest

# 設定測試環境變數 (必須在 import app 之前)
os.environ["TESTING"] = "1"

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

        # 重要的修復：在 drop_all 之前，確保所有 Session 已經關閉/移除
        db.session.remove()  # 移除當前的 session
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
