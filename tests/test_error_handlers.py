import pytest
from unittest.mock import patch
from sqlalchemy.exc import OperationalError, IntegrityError


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
            data="invalid json",
            content_type="application/json",
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert json_data["success"] is False

    def test_validation_error_response_format(self, client):
        """測試驗證錯誤回應格式"""
        res = client.post("/api/auth/register", json={})
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

    def test_database_operational_error(self, client, app, auth_headers):
        """測試資料庫操作錯誤"""
        with patch("app.models.user_model.User.get_by_id") as mock_get:
            mock_get.side_effect = OperationalError(
                "Database connection failed", None, None
            )

            response = client.get("/api/users/1", headers=auth_headers)

            assert response.status_code == 500
            assert response.json["success"] is False
            assert response.json["error"]["code"] == "DATABASE_ERROR"
            assert "database error" in response.json["error"]["message"].lower()
            assert "connection" not in response.json["error"]["message"].lower()

    def test_unexpected_exception(self, client, app, auth_headers):
        """測試未預期的異常"""
        with patch("app.models.user_model.User.get_by_id") as mock_get:
            mock_get.side_effect = ValueError("Unexpected value error")

            response = client.get("/api/users/1", headers=auth_headers)

            assert response.status_code == 500
            assert response.json["error"]["code"] == "INTERNAL_ERROR"
            assert "Unexpected value error" not in response.json["error"]["message"]

    def test_zero_division_error(self, client, app, auth_headers):
        """測試除以零錯誤"""
        with patch("app.models.user_model.User.get_by_id") as mock_get:
            mock_get.side_effect = ZeroDivisionError("division by zero")

            response = client.get("/api/users/1", headers=auth_headers)

            assert response.status_code == 500
            assert response.json["error"]["code"] == "INTERNAL_ERROR"

    @pytest.mark.parametrize(
        "exception,error_code",
        [
            (OperationalError("DB error", None, None), "DATABASE_ERROR"),
            (IntegrityError("Integrity error", None, None), "DATABASE_ERROR"),
            (Exception("Generic error"), "INTERNAL_ERROR"),
            (RuntimeError("Runtime error"), "INTERNAL_ERROR"),
        ],
    )
    def test_various_exceptions(self, client, auth_headers, exception, error_code):
        """測試各種異常類型"""
        with patch("app.models.user_model.User.get_by_id") as mock_get:
            mock_get.side_effect = exception

            response = client.get("/api/users/1", headers=auth_headers)

            assert response.status_code == 500
            assert response.json["error"]["code"] == error_code
