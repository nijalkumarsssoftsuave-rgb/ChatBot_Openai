import random
import time
import hashlib
from db.sqlite_db import get_connection

OTP_EXPIRY_SECONDS = 5 * 60  # 5 minutes

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

def hash_otp(otp: str) -> str:
    return hashlib.sha256(otp.encode()).hexdigest()


def save_otp(email: str, password: str, otp: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT OR REPLACE INTO user_otp
            (email, password, otp_hash, expires_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                email,
                password,              # TEMP plain password
                hash_otp(otp),
                int(time.time()) + OTP_EXPIRY_SECONDS
            )
        )
        conn.commit()
    finally:
        conn.close()

def verify_otp(email: str, otp: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT otp_hash, expires_at FROM user_otp WHERE email = ?",
            (email,)
        )
        row = cur.fetchone()

        if not row:
            return False

        otp_hash, expires_at = row

        if time.time() > expires_at:
            return False

        return hash_otp(otp) == otp_hash
    finally:
        conn.close()

def delete_otp(email: str):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM user_otp WHERE email = ?", (email,))
        conn.commit()
    finally:
        conn.close()
