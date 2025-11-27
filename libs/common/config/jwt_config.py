"""JWT 配置管理"""

from flask_jwt_extended import JWTManager
from app.models.user_model import User

jwt = JWTManager()


def register_jwt_callbacks(app):
    """註冊 JWT 回調函數"""
    jwt.init_app(app)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """自動載入當前使用者"""
        identity = jwt_data["sub"]
        return User.get_by_id(identity)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Token 過期處理"""
        return {
            "success": False,
            "error": {"code": "TOKEN_EXPIRED", "message": "Token has expired"},
        }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """無效 Token 處理"""
        return {
            "success": False,
            "error": {"code": "INVALID_TOKEN", "message": "Invalid token"},
        }, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        """缺少 Token 處理"""
        return {
            "success": False,
            "error": {
                "code": "MISSING_TOKEN",
                "message": "Missing authorization token",
            },
        }, 401

    return jwt
