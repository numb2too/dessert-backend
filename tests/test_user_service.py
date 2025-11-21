from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)


class TestGetUserService:
    """測試取得使用者 service"""

    def test_get_all_users_empty(self, app):
        users = get_all_users()
        assert users == []

    def test_get_all_users(self, app, sample_users):
        users = get_all_users()
        assert len(users) == 2

    def test_get_user_by_id_found(self, app, sample_users):
        user = get_user_by_id(1)
        assert user["name"] == "Alice"

    def test_get_user_by_id_not_found(self, app):
        user = get_user_by_id(999)
        assert user is None


class TestCreateUserService:
    """測試新增使用者 service"""

    def test_create_user(self, app):
        data = {"name": "Tony", "email": "tony@test.com"}
        user = create_user(data)
        assert user["name"] == "Tony"
        assert user["email"] == "tony@test.com"

    def test_create_user_default_name(self, app):
        user = create_user({})
        assert user["name"] == "No Name"


class TestUpdateUserService:
    """測試編輯使用者 service"""

    def test_update_user_success(self, app, sample_users):
        user = update_user(1, {"name": "Alice Updated"})
        assert user["name"] == "Alice Updated"

    def test_update_user_not_found(self, app):
        user = update_user(999, {"name": "Ghost"})
        assert user is None


class TestDeleteUserService:
    """測試刪除使用者 service"""

    def test_delete_user_success(self, app, sample_users):
        result = delete_user(1)
        assert result is True
        assert get_user_by_id(1) is None

    def test_delete_user_not_found(self, app):
        result = delete_user(999)
        assert result is False
