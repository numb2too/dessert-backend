from flask import Blueprint, request
from services.user_service import get_user_by_id, create_user

user_bp = Blueprint("users", __name__)

@user_bp.get("/<int:user_id>")
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return {"message": "User not found"}, 404
    return user, 200

@user_bp.post("/")
def add_user():
    data = request.json
    new_user = create_user(data)
    return new_user, 201
