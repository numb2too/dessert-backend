from apiflask import HTTPError
import logging
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


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

    # 取得 logger
    logger = logging.getLogger(__name__)

    @app.error_processor
    def custom_error_processor(error):
        """統一 HTTPError 回應格式"""
        extra_data = getattr(error, "extra_data", None) or {}
        error_code = extra_data.get("error_code", f"HTTP_{error.status_code}")

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

    # 處理資料庫錯誤
    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(error):
        """處理資料庫錯誤"""
        # ✅ 記錄完整錯誤到日誌
        logger.error(
            f"Database error occurred",
            exc_info=True,  # 包含完整 stack trace
            extra={"error_type": type(error).__name__, "error_detail": str(error)},
        )

        # ⚠️ 永遠不要在 API 回應中暴露資料庫結構
        return {
            "success": False,
            "error": {
                "code": "DATABASE_ERROR",
                "message": "A database error occurred. Please try again later.",
            },
        }, 500

    # 處理所有未捕獲的異常
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """處理未預期的錯誤"""
        # ✅ 記錄完整錯誤
        logger.error(
            f"Unexpected error occurred",
            exc_info=True,
            extra={
                "error_type": type(error).__name__,
            },
        )

        # ⚠️ 永遠不要暴露內部錯誤細節
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please contact support.",
            },
        }, 500

    # 處理 Werkzeug HTTP 異常
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """處理標準 HTTP 異常"""
        # 這些錯誤通常安全,可以顯示
        return {
            "success": False,
            "error": {
                "code": f"HTTP_{error.code}",
                "message": error.description,
            },
        }, error.code
