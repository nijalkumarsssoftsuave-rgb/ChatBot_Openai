# auth_db.py
from pymongo import MongoClient
from passlib.context import CryptContext
from utils.jwt_utils import _normalize_password
client = MongoClient("mongodb://localhost:27017")
db = client["rag_chat_db"]

users = db["users"]


from bcrypt import gensalt, hashpw, checkpw
def create_user(email: str, password: str):
    if users.find_one({"email": email}):
        return None

    password_bytes = _normalize_password(password)
    salt = gensalt()
    hashed_password = hashpw(password_bytes, salt).decode("utf-8")

    user = {
        "email": email,
        "password": hashed_password
    }

    users.insert_one(user)
    return user

def authenticate_user(email: str, password: str):
    user = users.find_one({"email": email})
    if not user:
        return None

    password_bytes = _normalize_password(password)
    stored_hash = user["password"].encode("utf-8")

    if not checkpw(password_bytes, stored_hash):
        return None

    return user
