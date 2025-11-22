from app import db
from app.models.user_model import User
from app.utils.error_handlers import ValidationError
from sqlalchemy.exc import IntegrityError


def get_all_users():
    users = User.query.all()
    return [u.to_dict() for u in users]


def get_user_by_id(user_id):
    user = db.session.get(User, user_id)
    return user.to_dict() if user else None


def create_user(data):
    user = User(name=data.get("name", "No Name"), email=data.get("email", ""))
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(
            message="Email already exists", extra_data={"error_code": "DUPLICATE_EMAIL"}
        )
    return user.to_dict()


def update_user(user_id, data):
    user = db.session.get(User, user_id)
    if not user:
        return None
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(
            message="Email already exists", extra_data={"error_code": "DUPLICATE_EMAIL"}
        )
    return user.to_dict()


def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
