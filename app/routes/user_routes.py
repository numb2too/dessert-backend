from apiflask import APIBlueprint, abort
from flask import request
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user,
)

user_bp = APIBlueprint("users", __name__, url_prefix="/users")


def success_response(data, status_code=200):
    """統一成功回應格式"""
    return {"success": True, "data": data}, status_code


# 取得所有使用者
@user_bp.get("/")
def list_users():
    users = get_all_users()
    return success_response(users)


# 取得單一使用者
@user_bp.get("/<int:user_id>")
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        abort(404, message="User not found", extra_data={"error_code": "NOT_FOUND"})
    return success_response(user)


# 新增使用者
@user_bp.post("/")
def add_user():
    data = request.json
    if not data:
        abort(
            400,
            message="Request body is required",
            extra_data={"error_code": "VALIDATION_ERROR"},
        )
    if not data.get("name"):
        abort(
            400,
            message="Name is required",
            extra_data={"error_code": "VALIDATION_ERROR"},
        )
    if not data.get("email"):
        abort(
            400,
            message="Email is required",
            extra_data={"error_code": "VALIDATION_ERROR"},
        )

    new_user = create_user(data)
    return success_response(new_user, 201)


# 編輯使用者
@user_bp.put("/<int:user_id>")
def edit_user(user_id):
    data = request.json
    if not data:
        abort(
            400,
            message="Request body is required",
            extra_data={"error_code": "VALIDATION_ERROR"},
        )

    user = update_user(user_id, data)
    if user is None:
        abort(404, message="User not found", extra_data={"error_code": "NOT_FOUND"})
    return success_response(user)


# 刪除使用者
@user_bp.delete("/<int:user_id>")
def remove_user(user_id):
    success = delete_user(user_id)
    if not success:
        abort(404, message="User not found", extra_data={"error_code": "NOT_FOUND"})
    return success_response({"message": "User deleted"})
