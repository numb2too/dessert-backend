import pytest
from app.models.user_model import User
from app import db


@pytest.fixture
def auth_headers(client):
    """建立認證用的 headers"""
    # 先註冊一個測試用戶
    client.post(
        "/api/auth/register",
        json={
            "email": "test_auth@example.com",
            "password": "Test1234!",
            "name": "Test Auth User",
        },
    )

    # 登入取得 token
    response = client.post(
        "/api/auth/login",
        json={"email": "test_auth@example.com", "password": "Test1234!"},
    )

    token = response.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_users(auth_headers):
    """建立測試用的使用者資料"""
    user1 = User(name="Alice", email="alice@example.com")
    user2 = User(name="Bob", email="bob@example.com")

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield [user1.id, user2.id]

    # 清理
    db.session.delete(user1)
    db.session.delete(user2)
    db.session.commit()


class TestGetUsers:
    """測試取得使用者"""

    def test_get_all_users_empty(self, client, auth_headers):
        res = client.get("/api/users/", headers=auth_headers)
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        # 至少會有登入的測試用戶
        assert isinstance(json_data["data"], list)

    def test_get_all_users(self, client, auth_headers, sample_users):
        res = client.get("/api/users/", headers=auth_headers)
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        # 應該至少有 3 個用戶（1 個認證用戶 + 2 個 sample_users）
        assert len(json_data["data"]) >= 2

    def test_get_user_success(self, client, auth_headers, sample_users):
        user_id = sample_users[0]
        res = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_get_user_not_found(self, client, auth_headers):
        res = client.get("/api/users/999", headers=auth_headers)
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"

    def test_get_user_without_auth(self, client, sample_users):
        """測試未登入時無法存取"""
        user_id = sample_users[0]
        res = client.get(f"/api/users/{user_id}")
        assert res.status_code == 401


class TestCreateUser:
    """測試新增使用者"""

    def test_create_user_success(self, client, auth_headers):
        res = client.post(
            "/api/users/",
            headers=auth_headers,
            json={"name": "Tony", "email": "tony@test.com"},
        )
        assert res.status_code == 201
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Tony"
        assert json_data["data"]["email"] == "tony@test.com"
        assert "id" in json_data["data"]

    def test_create_user_missing_name(self, client, auth_headers):
        res = client.post(
            "/api/users/", headers=auth_headers, json={"email": "test@test.com"}
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_create_user_missing_email(self, client, auth_headers):
        res = client.post("/api/users/", headers=auth_headers, json={"name": "Tony"})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_create_user_empty_body(self, client, auth_headers):
        res = client.post("/api/users/", headers=auth_headers, json={})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_create_user_without_auth(self, client):
        """測試未登入時無法新增"""
        res = client.post(
            "/api/users/", json={"name": "Tony", "email": "tony@test.com"}
        )
        assert res.status_code == 401


class TestUpdateUser:
    """測試編輯使用者"""

    def test_update_user_success(self, client, auth_headers, sample_users):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            headers=auth_headers,
            json={"name": "Alice Updated"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice Updated"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_update_user_email(self, client, auth_headers, sample_users):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            headers=auth_headers,
            json={"email": "alice_new@example.com"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["email"] == "alice_new@example.com"

    def test_update_user_not_found(self, client, auth_headers):
        res = client.put("/api/users/999", headers=auth_headers, json={"name": "Ghost"})
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"

    def test_update_user_empty_body(self, client, auth_headers, sample_users):
        user_id = sample_users[0]
        res = client.put(f"/api/users/{user_id}", headers=auth_headers, json={})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_update_user_without_auth(self, client, sample_users):
        """測試未登入時無法更新"""
        user_id = sample_users[0]
        res = client.put(f"/api/users/{user_id}", json={"name": "Alice Updated"})
        assert res.status_code == 401


class TestDeleteUser:
    """測試刪除使用者"""

    def test_delete_user_success(self, client, auth_headers, sample_users):
        user_id = sample_users[0]
        res = client.delete(f"/api/users/{user_id}", headers=auth_headers)
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["message"] == "User deleted"

        # 確認已刪除（軟刪除，會返回 404）
        res = client.get(f"/api/users/{user_id}", headers=auth_headers)
        assert res.status_code == 404

    def test_delete_user_not_found(self, client, auth_headers):
        res = client.delete("/api/users/999", headers=auth_headers)
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"

    def test_delete_user_without_auth(self, client, sample_users):
        """測試未登入時無法刪除"""
        user_id = sample_users[0]
        res = client.delete(f"/api/users/{user_id}")
        assert res.status_code == 401


class TestDuplicateEmail:
    """測試重複 email 的處理"""

    def test_create_user_duplicate_email(self, client, auth_headers, sample_users):
        """測試新增重複 email 的使用者"""
        res = client.post(
            "/api/users/",
            headers=auth_headers,
            json={"name": "Alice Clone", "email": "alice@example.com"},
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "DUPLICATE_EMAIL"
        assert json_data["error"]["message"] == "Email already exists"

    def test_update_user_duplicate_email(self, client, auth_headers, sample_users):
        """測試更新使用者時使用重複 email"""
        user_id = sample_users[1]  # Bob
        res = client.put(
            f"/api/users/{user_id}",
            headers=auth_headers,
            json={"email": "alice@example.com"},  # 使用 Alice 的 email
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "DUPLICATE_EMAIL"
        assert json_data["error"]["message"] == "Email already exists"
