"""認證相關的業務邏輯"""

from app import db
from app.models.user_model import User
from libs.common.utils.error_handlers import ValidationError, UnauthorizedError
from sqlalchemy.exc import IntegrityError


def register_user(data):
    """註冊新使用者"""
    # 驗證必填欄位
    if not data.get("email"):
        raise ValidationError(message="Email is required")
    if not data.get("password"):
        raise ValidationError(message="Password is required")
    if not data.get("name"):
        raise ValidationError(message="Name is required")

    # 檢查 email 是否已存在
    if User.get_by_email(data["email"]):
        raise ValidationError(
            message="Email already exists", extra_data={"error_code": "DUPLICATE_EMAIL"}
        )

    # 建立使用者
    user = User(name=data["name"], email=data["email"], phone=data.get("phone"))
    user.set_password(data["password"])

    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(
            message="Email already exists", extra_data={"error_code": "DUPLICATE_EMAIL"}
        )

    return user


def authenticate_user(email, password):
    """驗證使用者帳號密碼"""
    if not email or not password:
        raise ValidationError(message="Email and password are required")

    user = User.get_by_email(email)

    # 不透露具體是帳號還是密碼錯誤（安全性考量）
    if not user or not user.check_password(password):
        raise UnauthorizedError(message="Invalid email or password")

    if not user.is_active:
        raise UnauthorizedError(message="Account is disabled")

    return user


def change_password(user_id, old_password, new_password):
    """修改密碼"""
    if not old_password or not new_password:
        raise ValidationError(message="Old password and new password are required")

    if len(new_password) < 6:
        raise ValidationError(message="New password must be at least 6 characters")

    user = User.get_by_id(user_id)
    if not user:
        raise UnauthorizedError(message="User not found")

    # 驗證舊密碼
    if not user.check_password(old_password):
        raise UnauthorizedError(message="Invalid old password")

    # 設定新密碼
    user.set_password(new_password)
    db.session.commit()

    return user
