from bcrypt import gensalt, hashpw, checkpw
from utils.jwt_utils import _normalize_password
from db.sqlite_db import get_connection
from fastapi import HTTPException
import time
from app.service.otp_service import hash_otp

def user_exists(email: str) -> bool:
    email = email.strip().lower()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM users WHERE email = ? LIMIT 1",
            (email,)
        )
        return cur.fetchone() is not None
    finally:
        conn.close()

def create_user(email: str, password: str, role: str = "user"):
    email = email.strip().lower()
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

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

def verify_otp_and_create_user(email: str, otp: str) -> dict:
    """
    Verifies OTP and creates the user.
    Password hashing is handled inside create_user().
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT password, otp_hash, expires_at
            FROM user_otp
            WHERE email = ?
            """,
            (email,)
        )
        row = cur.fetchone()

        if not row:
            raise HTTPException(400, "OTP not found")

        password, otp_hash, expires_at = row

        if time.time() > expires_at:
            raise HTTPException(400, "OTP expired")

        if hash_otp(otp) != otp_hash:
            raise HTTPException(400, "Invalid OTP")

        user = create_user(email=email, password=password, role="user")
        if not user:
            raise HTTPException(400, "User already exists")

        cur.execute("DELETE FROM user_otp WHERE email = ?", (email,))
        conn.commit()

        return {"message": "Account verified successfully"}

    finally:
        conn.close()