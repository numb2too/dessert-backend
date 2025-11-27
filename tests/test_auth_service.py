"""測試認證服務層"""

import pytest
from app.services.auth_service import register_user, authenticate_user, change_password
from libs.common.utils.error_handlers import ValidationError, UnauthorizedError
from app.models.user_model import User
from app import db
from werkzeug.security import generate_password_hash


class TestRegisterUser:
    """測試使用者註冊"""

    def test_register_user_success(self, app):
        """測試成功註冊"""
        with app.app_context():
            user_data = {
                "name": "New User",
                "email": "newuser@example.com",
                "password": "password123",
                "phone": "0912345678",
            }

            user = register_user(user_data)

            assert user.id is not None
            assert user.name == "New User"
            assert user.email == "newuser@example.com"
            assert user.phone == "0912345678"
            assert user.is_active is True
            # 密碼應該被加密
            assert user.password != "password123"
            assert user.check_password("password123") is True

    def test_register_user_without_phone(self, app):
        """測試不提供電話號碼的註冊"""
        with app.app_context():
            user_data = {
                "name": "User",
                "email": "user@example.com",
                "password": "password123",
            }

            user = register_user(user_data)

            assert user.phone is None

    def test_register_user_missing_email(self, app):
        """測試缺少 email"""
        with app.app_context():
            user_data = {"name": "User", "password": "password123"}

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Email is required" in str(exc_info.value.message)

    def test_register_user_missing_password(self, app):
        """測試缺少密碼"""
        with app.app_context():
            user_data = {"name": "User", "email": "user@example.com"}

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Password is required" in str(exc_info.value.message)

    def test_register_user_missing_name(self, app):
        """測試缺少名稱"""
        with app.app_context():
            user_data = {"email": "user@example.com", "password": "password123"}

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Name is required" in str(exc_info.value.message)

    def test_register_user_duplicate_email(self, app):
        """測試重複的 email"""
        with app.app_context():
            # 先註冊一個使用者
            first_user = User(
                name="First User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(first_user)
            db.session.commit()

            # 嘗試用相同 email 註冊
            user_data = {
                "name": "Second User",
                "email": "test@example.com",
                "password": "password456",
            }

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Email already exists" in str(exc_info.value.message)

    def test_register_user_empty_email(self, app):
        """測試空 email"""
        with app.app_context():
            user_data = {"name": "User", "email": "", "password": "password123"}

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Email is required" in str(exc_info.value.message)

    def test_register_user_empty_password(self, app):
        """測試空密碼"""
        with app.app_context():
            user_data = {"name": "User", "email": "user@example.com", "password": ""}

            with pytest.raises(ValidationError) as exc_info:
                register_user(user_data)

            assert "Password is required" in str(exc_info.value.message)


class TestAuthenticateUser:
    """測試使用者認證"""

    def test_authenticate_user_success(self, app):
        """測試成功認證"""
        with app.app_context():
            # 創建測試使用者
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            # 認證
            authenticated = authenticate_user("test@example.com", "password123")

            assert authenticated.id == user.id
            assert authenticated.email == "test@example.com"

    def test_authenticate_user_wrong_password(self, app):
        """測試錯誤密碼"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(UnauthorizedError) as exc_info:
                authenticate_user("test@example.com", "wrongpassword")

            # 不應該透露具體是密碼錯誤
            assert "Invalid email or password" in str(exc_info.value.message)

    def test_authenticate_user_wrong_email(self, app):
        """測試錯誤 email"""
        with app.app_context():
            with pytest.raises(UnauthorizedError) as exc_info:
                authenticate_user("nonexistent@example.com", "password123")

            # 不應該透露具體是帳號不存在
            assert "Invalid email or password" in str(exc_info.value.message)

    def test_authenticate_user_inactive_account(self, app):
        """測試已停用的帳號"""
        with app.app_context():
            user = User(
                name="Inactive User",
                email="inactive@example.com",
                password=generate_password_hash("password123"),
                is_active=False,
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(UnauthorizedError) as exc_info:
                authenticate_user("inactive@example.com", "password123")

            assert "Account is disabled" in str(exc_info.value.message)

    def test_authenticate_user_missing_email(self, app):
        """測試缺少 email"""
        with app.app_context():
            with pytest.raises(ValidationError) as exc_info:
                authenticate_user("", "password123")

            assert "Email and password are required" in str(exc_info.value.message)

    def test_authenticate_user_missing_password(self, app):
        """測試缺少密碼"""
        with app.app_context():
            with pytest.raises(ValidationError) as exc_info:
                authenticate_user("test@example.com", "")

            assert "Email and password are required" in str(exc_info.value.message)

    def test_authenticate_user_case_sensitive_email(self, app):
        """測試 email 大小寫是否影響認證"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            # 根據你的實作,這可能成功或失敗
            # 如果 email 查詢不區分大小寫,應該成功
            try:
                authenticated = authenticate_user("TEST@example.com", "password123")
                # 如果成功,驗證是同一個使用者
                assert authenticated.id == user.id
            except UnauthorizedError:
                # 如果你的實作區分大小寫,這是預期行為
                pass


class TestChangePassword:
    """測試修改密碼"""

    def test_change_password_success(self, app):
        """測試成功修改密碼"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("oldpassword"),
            )
            db.session.add(user)
            db.session.commit()
            user_id = user.id

            result = change_password(user_id, "oldpassword", "newpassword")

            # 驗證密碼已更改
            updated_user = User.get_by_id(user_id)
            assert updated_user.check_password("newpassword") is True
            assert updated_user.check_password("oldpassword") is False

    def test_change_password_wrong_old_password(self, app):
        """測試舊密碼錯誤"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("oldpassword"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(UnauthorizedError) as exc_info:
                change_password(user.id, "wrongpassword", "newpassword")

            assert "Invalid old password" in str(exc_info.value.message)

    def test_change_password_user_not_found(self, app):
        """測試使用者不存在"""
        with app.app_context():
            with pytest.raises(UnauthorizedError) as exc_info:
                change_password(99999, "oldpassword", "newpassword")

            assert "User not found" in str(exc_info.value.message)

    def test_change_password_too_short(self, app):
        """測試新密碼太短"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("oldpassword"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(ValidationError) as exc_info:
                change_password(user.id, "oldpassword", "12345")  # 只有 5 個字元

            assert "at least 6 characters" in str(exc_info.value.message)

    def test_change_password_missing_old_password(self, app):
        """測試缺少舊密碼"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("oldpassword"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(ValidationError) as exc_info:
                change_password(user.id, "", "newpassword")

            assert "Old password and new password are required" in str(
                exc_info.value.message
            )

    def test_change_password_missing_new_password(self, app):
        """測試缺少新密碼"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("oldpassword"),
            )
            db.session.add(user)
            db.session.commit()

            with pytest.raises(ValidationError) as exc_info:
                change_password(user.id, "oldpassword", "")

            assert "Old password and new password are required" in str(
                exc_info.value.message
            )

    def test_change_password_same_as_old(self, app):
        """測試新密碼與舊密碼相同"""
        with app.app_context():
            user = User(
                name="Test User",
                email="test@example.com",
                password=generate_password_hash("password123"),
            )
            db.session.add(user)
            db.session.commit()

            # 使用相同的密碼應該可以成功（沒有限制）
            result = change_password(user.id, "password123", "password123")

            # 驗證密碼仍然有效
            updated_user = User.get_by_id(user.id)
            assert updated_user.check_password("password123") is True
