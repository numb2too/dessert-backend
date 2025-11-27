import os
import sys

# ✅ 添加項目根目錄到 Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ["FLASK_ENV"] = "testing"

from run import create_app
from app import db
from app.models.user_model import User
from flask_jwt_extended import create_access_token, decode_token
from werkzeug.security import generate_password_hash

app = create_app("testing")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

with app.app_context():
    db.create_all()

    # 創建使用者
    user = User(
        name="Test User",
        email="test@example.com",
        password=generate_password_hash("password123"),
    )
    db.session.add(user)
    db.session.commit()

    print(f"✅ User created: ID={user.id}, Email={user.email}")

    # 創建 token
    token = create_access_token(identity=str(user.id))
    print(f"✅ Token created: {token[:50]}...")

    # 解碼 token
    decoded = decode_token(token)
    print(f"✅ Token identity: {decoded['sub']}")

    # 查詢使用者
    found_user = User.get_by_id(decoded["sub"])
    print(f"✅ User lookup: {found_user}")

    # 測試 client
    client = app.test_client()
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

    print(f"\n{'='*50}")
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.get_json()}")
    print(f"{'='*50}")
