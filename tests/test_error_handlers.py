"""
測試 Error Handlers 的回應格式
"""


class TestErrorResponses:
    """測試錯誤回應格式"""

    def test_not_found_response_format(self, client, auth_token):
        """測試 404 回應格式"""
        res = client.get(
            "/api/users/999",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"
        assert json_data["error"]["message"] == "User not found"

    def test_bad_request_error(self, client):
        """測試 400 錯誤請求(無效 JSON)"""
        res = client.post(
            "/api/auth/register",
            data="invalid json",  # 不是有效的 JSON
            content_type="application/json",
        )

        # 無效 JSON 應該返回 400
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False

    def test_validation_error_response_format(self, client):
        """測試驗證錯誤回應格式"""
        res = client.post(
            "/api/auth/register", json={}  # 改用註冊端點  # 空 JSON 會觸發驗證錯誤
        )
        # ✅ APIFlask 對驗證錯誤返回 422
        assert res.status_code == 422
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "HTTP_422"

    def test_http_404_response_format(self, client):
        """測試不存在的路由"""
        res = client.get("/api/nonexistent")
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "HTTP_404"

    def test_http_405_response_format(self, client):
        """測試不允許的方法"""
        res = client.patch("/api/users/1")
        assert res.status_code == 405
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "HTTP_405"
