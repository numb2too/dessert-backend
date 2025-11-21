from app import db
from app.models.user_model import User


def get_all_users():
    users = User.query.all()
    return [u.to_dict() for u in users]


def get_user_by_id(user_id):
    # 修正:使用 db.session.get() 替代 User.query.get()
    user = db.session.get(User, user_id)
    return user.to_dict() if user else None


def create_user(data):
    user = User(name=data.get("name", "No Name"), email=data.get("email", ""))
    db.session.add(user)
    db.session.commit()
    return user.to_dict()


def update_user(user_id, data):
    # 修正:使用 db.session.get() 替代 User.query.get()
    user = db.session.get(User, user_id)
    if not user:
        return None
    if "name" in data:
        user.name = data["name"]
    if "email" in data:
        user.email = data["email"]
    db.session.commit()
    return user.to_dict()


def delete_user(user_id):
    # 修正:使用 db.session.get() 替代 User.query.get()
    user = db.session.get(User, user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
