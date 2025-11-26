from apiflask import APIBlueprint
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, current_user
from app.services.auth_service import register_user, authenticate_user, change_password
from libs.common.utils.response_helper import success_response
from libs.common.utils.schemas import (
    RegisterSchema,
    LoginSchema,
    ChangePasswordSchema,
    TokenResponseSchema,
    UserProfileSchema,
)

auth_bp = APIBlueprint("auth", __name__, tag="Authentication")


@auth_bp.post("/register")
@auth_bp.input(RegisterSchema)
@auth_bp.output(TokenResponseSchema, status_code=201)
def register(json_data):
    """註冊新使用者"""
    user = register_user(json_data)

    # 註冊成功後自動產生 JWT token
    access_token = create_access_token(identity=user.id)

    return success_response({"access_token": access_token, "user": user.to_dict()}, 201)


@auth_bp.post("/login")
@auth_bp.input(LoginSchema)
@auth_bp.output(TokenResponseSchema)
def login(json_data):
    """使用者登入"""
    user = authenticate_user(json_data["email"], json_data["password"])

    # 產生 JWT token
    access_token = create_access_token(identity=user.id)

    return success_response({"access_token": access_token, "user": user.to_dict()})


@auth_bp.get("/me")
@jwt_required()
@auth_bp.output(UserProfileSchema)
def get_current_user():
    """取得當前登入使用者資訊"""
    return success_response(current_user.to_dict())


@auth_bp.post("/change-password")
@jwt_required()
@auth_bp.input(ChangePasswordSchema)
def change_user_password(json_data):
    """修改密碼"""
    change_password(
        current_user.id, json_data["old_password"], json_data["new_password"]
    )

    return success_response({"message": "Password changed successfully"})
