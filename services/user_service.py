from models.user_model import users, next_id

def get_user_by_id(user_id):
    return users.get(user_id)

def create_user(data):
    global next_id
    user = {
        "id": next_id,
        "name": data.get("name", "No Name"),
        "email": data.get("email", ""),
    }
    users[next_id] = user
    next_id += 1
    return user
