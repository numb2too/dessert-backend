import pytest
from app.models.user_model import User


class TestRegister:
    """測試註冊功能"""

    def test_register_success(self, client):
        """測試成功註冊"""
        res = client.post(
            "/api/auth/register",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["user"]["email"] == "test@example.com"

    def test_register_duplicate_email(self, client, sample_users):
        """測試重複 email"""
        res = client.post(
            "/api/auth/register",
            json={
                "name": "Duplicate",
                "email": "alice@example.com",
                "password": "password123",
            },
        )
        assert res.status_code == 400
        data = res.get_json()
        assert data["success"] is False
        assert "already exists" in data["error"]["message"].lower()

    def test_register_weak_password(self, client):
        """測試密碼太短"""
        res = client.post(
            "/api/auth/register",
            json={"name": "Test User", "email": "test@example.com", "password": "123"},
        )
        assert res.status_code == 422
        data = res.get_json()
        assert data["success"] is False

    def test_register_missing_fields(self, client):
        """測試缺少必填欄位"""
        res = client.post("/api/auth/register", json={"email": "test@example.com"})
        assert res.status_code == 422
        data = res.get_json()
        assert data["success"] is False
        assert "error" in data
        assert data["error"]["code"] == "HTTP_422"


class TestLogin:
    """測試登入功能"""

    def test_login_success(self, client, sample_users):
        """測試成功登入"""
        res = client.post(
            "/api/auth/login",
            json={"email": "alice@example.com", "password": "password123"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["user"]["email"] == "alice@example.com"

    def test_login_wrong_password(self, client, sample_users):
        """測試密碼錯誤"""
        res = client.post(
            "/api/auth/login",
            json={"email": "alice@example.com", "password": "wrongpassword"},
        )
        assert res.status_code == 401
        data = res.get_json()
        assert data["success"] is False

    def test_login_nonexistent_user(self, client):
        """測試不存在的使用者"""
        res = client.post(
            "/api/auth/login",
            json={"email": "ghost@example.com", "password": "password123"},
        )
        assert res.status_code == 401


class TestGetCurrentUser:
    """測試取得當前使用者"""

    def test_get_current_user_success(self, client, auth_token):
        """測試成功取得"""
        res = client.get(
            "/api/auth/me", headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True
        assert data["data"]["name"] == "Alice"
        assert "email" in data["data"]

    def test_get_current_user_no_token(self, client):
        """測試缺少 token"""
        res = client.get("/api/auth/me")
        assert res.status_code == 401


class TestChangePassword:
    """測試修改密碼"""

    def test_change_password_success(self, client, auth_token):
        """測試成功修改密碼"""
        res = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"old_password": "password123", "new_password": "newpassword123"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["success"] is True

    def test_change_password_wrong_old(self, client, auth_token):
        """測試舊密碼錯誤"""
        res = client.post(
            "/api/auth/change-password",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"old_password": "wrongpassword", "new_password": "newpassword123"},
        )
        assert res.status_code == 401
