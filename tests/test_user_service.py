"""測試使用者服務層"""

import pytest
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from libs.common.utils.error_handlers import ValidationError, NotFoundError
from app.models.user_model import User
from app import db
from werkzeug.security import generate_password_hash


class TestGetAllUsers:
    """測試取得所有使用者"""

    def test_get_all_users_empty(self, app):
        """測試空資料庫"""
        with app.app_context():
            users = get_all_users()
            assert users == []

    def test_get_all_users_with_data(self, app):
        """測試有資料時取得所有使用者"""
        with app.app_context():
            # 創建測試資料
            user1 = User(
                name="Alice",
                email="alice@example.com",
                password=generate_password_hash("password123"),
            )
            user2 = User(
                name="Bob",
                email="bob@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add_all([user1, user2])
            db.session.commit()

            users = get_all_users()

            assert len(users) == 2
            assert users[0]["name"] == "Alice"
            assert users[1]["name"] == "Bob"
            # 確認不返回密碼
            assert "password" not in users[0]

    def test_get_all_users_includes_inactive(self, app):
        """測試是否包含已停用的使用者"""
        with app.app_context():
            active_user = User(
                name="Active",
                email="active@example.com",
                password=generate_password_hash("password123"),
                is_active=True,
            )
            inactive_user = User(
                name="Inactive",
                email="inactive@example.com",
                password=generate_password_hash("password123"),
                is_active=False,
            )
            db.session.add_all([active_user, inactive_user])
            db.session.commit()

            users = get_all_users()

            # 根據你的業務邏輯調整
            # 如果應該包含 inactive，assert len(users) == 2
            # 如果應該排除 inactive，assert len(users) == 1
            assert len(users) == 2  # 目前你的實作包含所有使用者


class TestGetUserById:
    """測試取得單一使用者"""

    def test_get_user_by_id_success(self, app):
        """測試成功取得使用者"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            result = get_user_by_id(user.id)

            assert result["id"] == user.id
            assert result["name"] == "Test User"
            assert result["email"] == "test@example.com"
            assert "password" not in result

    def test_get_user_by_id_not_found(self, app):
        """測試使用者不存在"""
        with app.app_context():
            with pytest.raises(NotFoundError) as exc_info:
                get_user_by_id(99999)

            assert "User not found" in str(exc_info.value.message)

    def test_get_user_by_id_invalid_type(self, app):
        """測試無效的 ID 類型"""
        with app.app_context():
            # 如果傳入字串，應該如何處理？
            with pytest.raises((NotFoundError)) as exc_info:
                get_user_by_id("invalid")

            assert "User not found" in str(exc_info.value.message)


class TestUpdateUser:
    """測試更新使用者"""

    def test_update_user_name(self, app):
        """測試更新使用者名稱"""
        with app.app_context():
            user = User(
                name="Original Name",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            result = update_user(user_id, {"name": "Updated Name"})

            assert result["name"] == "Updated Name"
            assert result["email"] == "test@example.com"  # 未改變

    def test_update_user_phone(self, app):
        """測試更新電話"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            result = update_user(user.id, {"phone": "0912345678"})

            assert result["phone"] == "0912345678"

    def test_update_user_email(self, app):
        """測試更新 email"""
        with app.app_context():
            user = User(
                name="Test",
                email="old@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            result = update_user(user.id, {"email": "new@example.com"})

            assert result["email"] == "new@example.com"

    def test_update_user_duplicate_email(self, app):
        """測試更新為已存在的 email"""
        with app.app_context():
            user1 = User(
                name="User 1",
                email="user1@example.com",
                password=generate_password_hash("password123"),
            )
            user2 = User(
                name="User 2",
                email="user2@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add_all([user1, user2])
            db.session.commit()

            # 嘗試將 user2 的 email 改為 user1 的 email
            with pytest.raises(ValidationError) as exc_info:
                update_user(user2.id, {"email": "user1@example.com"})

            assert "Email already exists" in str(exc_info.value.message)

    def test_update_user_same_email(self, app):
        """測試更新為自己的 email（應該允許）"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            # 更新為相同的 email 應該成功
            result = update_user(user.id, {"email": "test@example.com"})

            assert result["email"] == "test@example.com"

    def test_update_user_empty_data(self, app):
        """測試空資料"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(ValidationError) as exc_info:
                update_user(user.id, {})

            assert "Request body is required" in str(exc_info.value.message)

    def test_update_user_not_found(self, app):
        """測試更新不存在的使用者"""
        with app.app_context():
            with pytest.raises(NotFoundError):
                update_user(99999, {"name": "Ghost"})

    def test_update_user_multiple_fields(self, app):
        """測試同時更新多個欄位"""
        with app.app_context():
            user = User(
                name="Old Name",
                email="old@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            result = update_user(
                user.id,
                {"name": "New Name", "email": "new@example.com", "phone": "0987654321"},
            )

            assert result["name"] == "New Name"
            assert result["email"] == "new@example.com"
            assert result["phone"] == "0987654321"

    def test_update_user_ignores_unknown_fields(self, app):
        """測試忽略未知欄位"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            # 傳入未定義的欄位
            result = update_user(
                user.id, {"name": "New Name", "unknown_field": "should be ignored"}
            )

            assert result["name"] == "New Name"
            # unknown_field 應該被忽略


class TestDeleteUser:
    """測試刪除使用者"""

    def test_delete_user_success(self, app):
        """測試成功刪除使用者（軟刪除）"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            result = delete_user(user_id)

            assert result is True

            # 驗證使用者被標記為 inactive
            deleted_user = User.get_by_id(user_id)
            assert deleted_user is not None  # 仍存在資料庫
            assert deleted_user.is_active is False  # 但已停用

    def test_delete_user_not_found(self, app):
        """測試刪除不存在的使用者"""
        with app.app_context():
            with pytest.raises(NotFoundError):
                delete_user(99999)

    def test_delete_user_already_inactive(self, app):
        """測試刪除已經被停用的使用者"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
                is_active=False,
            )
            db.session.add(user)
            db.session.commit()

            # 應該仍然成功
            result = delete_user(user.id)
            assert result is True

    def test_delete_user_idempotent(self, app):
        """測試刪除操作是冪等的（多次刪除結果相同）"""
        with app.app_context():
            user = User(
                name="Test",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            # 第一次刪除
            delete_user(user_id)
            # 第二次刪除應該仍然成功（或根據業務邏輯決定）
            result = delete_user(user_id)

            assert result is True
            assert User.get_by_id(user_id).is_active is False
