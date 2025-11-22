class TestGetUsers:
    """測試取得使用者"""

    def test_get_all_users_empty(self, client):
        res = client.get("/api/users/")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"] == []

    def test_get_all_users(self, client, sample_users):
        res = client.get("/api/users/")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert len(json_data["data"]) == 2

    def test_get_user_success(self, client, sample_users):
        user_id = sample_users[0]
        res = client.get(f"/api/users/{user_id}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_get_user_not_found(self, client):
        res = client.get("/api/users/999")
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"


class TestCreateUser:
    """測試新增使用者"""

    def test_create_user_success(self, client):
        res = client.post(
            "/api/users/",
            json={"name": "Tony", "email": "tony@test.com"},
        )
        assert res.status_code == 201
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Tony"
        assert json_data["data"]["email"] == "tony@test.com"
        assert "id" in json_data["data"]

    def test_create_user_missing_name(self, client):
        res = client.post("/api/users/", json={"email": "test@test.com"})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_create_user_missing_email(self, client):
        res = client.post("/api/users/", json={"name": "Tony"})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

    def test_create_user_empty_body(self, client):
        res = client.post("/api/users/", json={})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"


class TestUpdateUser:
    """測試編輯使用者"""

    def test_update_user_success(self, client, sample_users):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            json={"name": "Alice Updated"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice Updated"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_update_user_email(self, client, sample_users):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            json={"email": "alice_new@example.com"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["email"] == "alice_new@example.com"

    def test_update_user_not_found(self, client):
        res = client.put("/api/users/999", json={"name": "Ghost"})
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"

    def test_update_user_empty_body(self, client, sample_users):
        user_id = sample_users[0]
        res = client.put(f"/api/users/{user_id}", json={})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"


class TestDeleteUser:
    """測試刪除使用者"""

    def test_delete_user_success(self, client, sample_users):
        user_id = sample_users[0]
        res = client.delete(f"/api/users/{user_id}")
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["message"] == "User deleted"

        # 確認已刪除
        res = client.get(f"/api/users/{user_id}")
        assert res.status_code == 404

    def test_delete_user_not_found(self, client):
        res = client.delete("/api/users/999")
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"
