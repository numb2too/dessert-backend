"""
測試 Error Handlers 的回應格式
"""


class TestErrorResponses:
    """測試錯誤回應格式"""

    def test_not_found_response_format(self, client):
        """測試 404 回應格式"""
        res = client.get("/api/users/999")
        assert res.status_code == 404
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "NOT_FOUND"
        assert json_data["error"]["message"] == "User not found"

    def test_validation_error_response_format(self, client):
        """測試 400 驗證錯誤回應格式"""
        res = client.post("/api/users/", json={})
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False
        assert json_data["error"]["code"] == "VALIDATION_ERROR"

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
