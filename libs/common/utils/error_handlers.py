from apiflask import HTTPError


class NotFoundError(HTTPError):
    """404 資源不存在錯誤"""

    status_code = 404

    def __init__(self, message="Resource not found", extra_data=None):
        self.message = message
        self.extra_data = extra_data or {"error_code": "NOT_FOUND"}
        super().__init__()


class ValidationError(HTTPError):
    """驗證錯誤"""

    status_code = 422

    def __init__(self, message="Validation failed", extra_data=None):
        self.message = message
        self.extra_data = extra_data or {"error_code": "VALIDATION_ERROR"}
        super().__init__()


class UnauthorizedError(HTTPError):
    """401 未授權錯誤"""

    status_code = 401

    def __init__(self, message="Unauthorized", extra_data=None):
        self.message = message
        self.extra_data = extra_data or {"error_code": "UNAUTHORIZED"}
        super().__init__()


def register_error_handlers(app):
    """註冊自訂錯誤回應格式"""

    @app.error_processor
    def custom_error_processor(error):
        """統一錯誤回應格式"""
        # extra_data 可能是 None、空 dict 或有值
        extra_data = getattr(error, "extra_data", None) or {}
        error_code = extra_data.get("error_code", f"HTTP_{error.status_code}")

        # message 可能在 error.message 或 error.detail
        message = getattr(error, "message", None) or getattr(
            error, "detail", "Unknown error"
        )

        return (
            {
                "success": False,
                "error": {
                    "code": error_code,
                    "message": message,
                },
            },
            error.status_code,
            error.headers,
        )
