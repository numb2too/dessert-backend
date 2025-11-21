from flask import Blueprint, request
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)

user_bp = Blueprint("users", __name__)


# 取得所有使用者
@user_bp.get("/")
def list_users():
    users = get_all_users()
    return users, 200


# 取得單一使用者
@user_bp.get("/<int:user_id>")
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return {"message": "User not found"}, 404
    return user, 200


# 新增使用者
@user_bp.post("/")
def add_user():
    data = request.json
    new_user = create_user(data)
    return new_user, 201


# 編輯使用者
@user_bp.put("/<int:user_id>")
def edit_user(user_id):
    data = request.json
    user = update_user(user_id, data)
    if user is None:
        return {"message": "User not found"}, 404
    return user, 200


# 刪除使用者
@user_bp.delete("/<int:user_id>")
def remove_user(user_id):
    success = delete_user(user_id)
    if not success:
        return {"message": "User not found"}, 404
    return {"message": "User deleted"}, 200
