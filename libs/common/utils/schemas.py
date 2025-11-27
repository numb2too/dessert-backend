from apiflask import Schema
from apiflask.fields import String, Integer, Boolean, Nested
from apiflask.validators import Length, Email
from marshmallow import validates, ValidationError


class RegisterSchema(Schema):
    """註冊 Schema"""

    name = String(
        required=True,
        validate=Length(min=1, max=100),
        metadata={"description": "name", "example": "test111"},
    )
    email = String(
        required=True,
        validate=Email(),
        metadata={"description": "email", "example": "test111@example.com"},
    )
    password = String(
        required=True,
        validate=Length(min=6, error="Password must be at least 6 characters"),
        metadata={"description": "password", "example": "password123"},
    )
    phone = String(
        validate=Length(max=20),
        metadata={"description": "phone", "example": "0912345678"},
    )


class LoginSchema(Schema):
    """登入 Schema"""

    email = String(
        required=True, validate=Email(), metadata={"example": "test1@example.com"}
    )
    password = String(required=True, metadata={"example": "test1"})


class ChangePasswordSchema(Schema):
    """修改密碼 Schema"""

    old_password = String(required=True)
    new_password = String(required=True, validate=Length(min=6))


class UserProfileSchema(Schema):
    """使用者資料 Schema"""

    id = Integer()
    name = String()
    email = String()
    phone = String()
    is_active = Boolean()
    created_at = String()
    updated_at = String()


class UserResponseSchema(Schema):
    success = Boolean(required=True)
    data = Nested(UserProfileSchema, required=True)


class TokenDataSchema(Schema):
    access_token = String(required=True)
    user = Nested(UserProfileSchema, required=True)


class TokenResponseSchema(Schema):
    success = Boolean(required=True)
    data = Nested(TokenDataSchema, required=True)


# 定義更新使用者的 Schema
class UpdateUserSchema(Schema):
    name = String(validate=Length(min=1, max=100), required=False)
    email = String(required=False)
    phone = String(validate=Length(max=20), required=False)


class UpdateDataSchema(Schema):
    id = Integer()
    name = String()
    email = String()
    name = String()


class UpdateResponseSchema(Schema):
    success = Boolean(required=True)
    data = Nested(UpdateDataSchema, required=True)
