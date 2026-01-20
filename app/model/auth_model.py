from bcrypt import gensalt, hashpw, checkpw
from utils.jwt_utils import _normalize_password
from db.sqlite_db import get_connection

def create_user(email: str, password: str, role: str = "user"):
    email = email.strip().lower()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))

        if cur.fetchone():
            return None

        password_bytes = _normalize_password(password)
        hashed_password = hashpw(password_bytes, gensalt()).decode("utf-8")

        cur.execute(
            "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
            (email, hashed_password, role)
        )
        conn.commit()
        return {
            "id": cur.lastrowid,
            "email": email,
            "role": role
        }
    finally:
        if conn is not None:
            conn.close()

def authenticate_user(email: str, password: str):
    email = email.strip().lower()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, password, role FROM users WHERE email = ?",
            (email,)
        )
        row = cur.fetchone()
        if not row:
            return None
        user_id, stored_hash, role = row
        if not checkpw(_normalize_password(password), stored_hash.encode()):
            return None
        return {
            "id": user_id,
            "email": email,
            "role": role
        }
    finally:
        if conn is not None:
            conn.close()
