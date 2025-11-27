class TestGetUsers:
    """測試取得使用者"""

    def test_get_all_users(self, client, auth_token):
        res = client.get(
            "/api/users/",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert len(json_data["data"]) == 2

    def test_get_user_success(self, client, sample_users, auth_token):
        user_id = sample_users[0]
        res = client.get(
            f"/api/users/{user_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_get_user_not_found(self, client, auth_token):
        res = client.get(
            "/api/users/999",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"


class TestUpdateUser:
    """測試編輯使用者"""

    def test_update_user_success(self, client, sample_users, auth_token):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            json={"name": "Alice Updated"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["name"] == "Alice Updated"
        assert json_data["data"]["email"] == "alice@example.com"

    def test_update_user_email(self, client, sample_users, auth_token):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            json={"email": "alice_new@example.com"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["email"] == "alice_new@example.com"

    def test_update_user_not_found(self, client, auth_token):
        res = client.put(
            "/api/users/999",
            json={"name": "Ghost"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"

    def test_update_user_empty_body(self, client, sample_users, auth_token):
        user_id = sample_users[0]
        res = client.put(
            f"/api/users/{user_id}",
            json={},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 422
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"


class TestDeleteUser:
    """測試刪除使用者"""

    def test_delete_user_success(self, client, sample_users, auth_token):
        user_id = sample_users[0]
        res = client.delete(
            f"/api/users/{user_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 200
        json_data = res.get_json()
        assert json_data["success"] is True
        assert json_data["data"]["message"] == "User deleted"

        # 確認已刪除
        res = client.get(
            f"/api/users/{user_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        # 如果是軟刪除，且 API 設計為回傳 200
        assert res.status_code == 200
        assert res.get_json()["data"]["is_active"] is False

    def test_delete_user_not_found(self, client, auth_token):
        res = client.delete(
            "/api/users/999",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"


class TestDuplicateEmail:
    """測試重複 email 的處理"""

    def test_update_user_duplicate_email(self, client, sample_users, auth_token):
        """測試更新使用者時使用重複 email"""
        user_id = sample_users[1]  # Bob
        res = client.put(
            f"/api/users/{user_id}",
            json={"email": "alice@example.com"},  # 使用 Alice 的 email
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 422
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "DUPLICATE_EMAIL"
        assert json_data["error"]["message"] == "Email already exists"
