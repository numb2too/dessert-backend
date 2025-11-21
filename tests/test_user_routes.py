class TestGetUsers:
    """測試取得使用者"""

    def test_get_all_users_empty(self, client):
        res = client.get("/api/users/")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_get_all_users(self, client, sample_users):
        res = client.get("/api/users/")
        assert res.status_code == 200
        data = res.get_json()
        assert len(data) == 2

    def test_get_user_success(self, client, sample_users):
        res = client.get("/api/users/1")
        assert res.status_code == 200
        data = res.get_json()
        assert data["name"] == "Alice"
        assert data["email"] == "alice@example.com"

    def test_get_user_not_found(self, client):
        res = client.get("/api/users/999")
        assert res.status_code == 404
        assert res.get_json()["message"] == "User not found"


class TestCreateUser:
    """測試新增使用者"""

    def test_create_user_success(self, client):
        res = client.post(
            "/api/users/",
            json={"name": "Tony", "email": "tony@test.com"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["name"] == "Tony"
        assert data["email"] == "tony@test.com"
        assert "id" in data

    def test_create_user_minimal(self, client):
        res = client.post("/api/users/", json={})
        assert res.status_code == 201
        data = res.get_json()
        assert data["name"] == "No Name"


class TestUpdateUser:
    """測試編輯使用者"""

    def test_update_user_success(self, client, sample_users):
        res = client.put(
            "/api/users/1",
            json={"name": "Alice Updated"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["name"] == "Alice Updated"
        assert data["email"] == "alice@example.com"

    def test_update_user_email(self, client, sample_users):
        res = client.put(
            "/api/users/1",
            json={"email": "alice_new@example.com"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["email"] == "alice_new@example.com"

    def test_update_user_not_found(self, client):
        res = client.put(
            "/api/users/999",
            json={"name": "Ghost"},
        )
        assert res.status_code == 404


class TestDeleteUser:
    """測試刪除使用者"""

    def test_delete_user_success(self, client, sample_users):
        res = client.delete("/api/users/1")
        assert res.status_code == 200
        assert res.get_json()["message"] == "User deleted"

        # 確認已刪除
        res = client.get("/api/users/1")
        assert res.status_code == 404

    def test_delete_user_not_found(self, client):
        res = client.delete("/api/users/999")
        assert res.status_code == 404
