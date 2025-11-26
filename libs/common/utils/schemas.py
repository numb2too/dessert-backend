from apiflask import Schema
from apiflask.fields import String, Integer, Boolean, Nested
from apiflask.validators import Length, Email


class RegisterSchema(Schema):
    """註冊 Schema"""

    name = String(required=True, validate=Length(min=1, max=100))
    email = String(required=True, validate=Email())
    password = String(
        required=True,
        validate=Length(min=6, error="Password must be at least 6 characters"),
    )
    phone = String(validate=Length(max=20))


class LoginSchema(Schema):
    """登入 Schema"""

    email = String(required=True, validate=Email())
    password = String(required=True)


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


class TokenDataSchema(Schema):
    access_token = String(required=True)
    user = Nested(UserProfileSchema, required=True)


class TokenResponseSchema(Schema):
    success = Boolean(required=True)
    data = Nested(TokenDataSchema, required=True)
