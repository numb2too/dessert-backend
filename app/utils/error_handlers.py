from apiflask import HTTPError


class NotFoundError(HTTPError):
    """資源不存在"""

    status_code = 404
    message = "Resource not found"
    extra_data = {"error_code": "NOT_FOUND"}


class ValidationError(HTTPError):
    """驗證錯誤"""

    status_code = 400
    message = "Validation failed"
    extra_data = {"error_code": "VALIDATION_ERROR"}


class UnauthorizedError(HTTPError):
    """未授權"""

    status_code = 401
    message = "Unauthorized"
    extra_data = {"error_code": "UNAUTHORIZED"}


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
