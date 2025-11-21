from app.services.user_service import create_user, get_user_by_id
from app.models.user_model import users, next_id


def setup_function():
    # 讓每個測試重新初始化假資料
    users.clear()
    users[1] = {"id": 1, "name": "Alice", "email": "alice@example.com"}
    users[2] = {"id": 2, "name": "Bob", "email": "bob@example.com"}

    global next_id
    next_id = 3


def test_get_user_by_id_found():
    user = get_user_by_id(1)
    assert user["name"] == "Alice"


def test_get_user_by_id_not_found():
    user = get_user_by_id(999)
    assert user is None


def test_create_user():
    data = {"name": "Tony", "email": "tony@test.com"}
    new_user = create_user(data)
    assert new_user["id"] == 4
    assert new_user["name"] == "Tony"
