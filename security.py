from werkzeug.security import safe_str_cmp
from db_dealer import UserDealer
from models.usermodel import UserModel


def authenticate(username, password):
    reckon = UserDealer.find_by_column(username, "username")
    if reckon:
        user = UserModel(*reckon.values())
        if safe_str_cmp(user.password, password):
            return user


def identity(payload):
    user_id = payload["identity"]
    return UserDealer.find_by_column(user_id, "id")
