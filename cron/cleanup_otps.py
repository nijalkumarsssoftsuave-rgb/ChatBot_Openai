import time
from db.sqlite_db import get_connection


def cleanup_expired_otps():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM user_otp WHERE expires_at < ?",
            (int(time.time()),)
        )
        conn.commit()
    finally:
        conn.close()
if __name__ == "__main__":
    cleanup_expired_otps()
