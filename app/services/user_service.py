from app import db
from app.models.user_model import User
from libs.common.utils.error_handlers import ValidationError, NotFoundError
from sqlalchemy.exc import IntegrityError


def get_all_users():
    """取得所有使用者"""
    users = User.query.all()
    return [u.to_dict() for u in users]


def get_user_by_id(user_id):
    """取得單一使用者"""
    user = User.get_by_id(user_id)
    if not user:
        raise NotFoundError(message="User not found")
    return user.to_dict()


def update_user(user_id, data):
    """更新使用者資料（不包含密碼）"""
    if not data:
        raise ValidationError(message="Request body is required")

    user = User.get_by_id(user_id)
    if not user:
        raise NotFoundError(message="User not found")

    # 只允許更新特定欄位
    if "name" in data:
        user.name = data["name"]
    if "phone" in data:
        user.phone = data["phone"]

    # Email 更新需要額外檢查
    if "email" in data and data["email"] != user.email:
        existing_user = User.get_by_email(data["email"])
        if existing_user:
            raise ValidationError(
                message="Email already exists",
                extra_data={"error_code": "DUPLICATE_EMAIL"},
            )
        user.email = data["email"]

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(
            message="Email already exists", extra_data={"error_code": "DUPLICATE_EMAIL"}
        )

    return user.to_dict()


def delete_user(user_id):
    """刪除使用者（軟刪除）"""
    user = User.get_by_id(user_id)
    if not user:
        raise NotFoundError(message="User not found")

    # 軟刪除：只標記為 inactive
    user.is_active = False
    db.session.commit()
    return True
