from bcrypt import gensalt, hashpw, checkpw
from utils.jwt_utils import _normalize_password
from db.sqlite_db import get_connection

def create_user(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cur.fetchone():
        conn.close()
        return None

    password_bytes = _normalize_password(password)
    hashed_password = hashpw(password_bytes, gensalt()).decode("utf-8")

    cur.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email, hashed_password)
    )
    conn.commit()

    user_id = cur.lastrowid
    conn.close()

    return {"id": user_id, "email": email}

def authenticate_user(email: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE email = ?",
        (email,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    user_id, stored_hash = row
    password_bytes = _normalize_password(password)

    if not checkpw(password_bytes, stored_hash.encode("utf-8")):
        return None

    return {"id": user_id, "email": email}
