from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, current_user
from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from libs.common.utils.response_helper import success_response
from libs.common.utils.schemas import UserProfileSchema
from flask import request

user_bp = APIBlueprint("users", __name__, tag="Users")


@user_bp.get("/profile")
@jwt_required()
@user_bp.output(UserProfileSchema)
def profile():
    """取得個人資料"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }


@user_bp.get("/")
@jwt_required()
def list_users():
    """取得所有使用者"""
    users = get_all_users()
    return success_response(users)


@user_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    """取得單一使用者"""
    user = get_user_by_id(user_id)
    return success_response(user)


@user_bp.put("/<int:user_id>")
@jwt_required()
def edit_user(user_id):
    """更新使用者"""
    user = update_user(user_id, request.json or {})
    return success_response(user)


@user_bp.delete("/<int:user_id>")
@jwt_required()
def remove_user(user_id):
    """刪除使用者"""
    delete_user(user_id)
    return success_response({"message": "User deleted"})
