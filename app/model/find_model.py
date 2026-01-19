from db.sqlite_db import get_connection

def get_user_by_id(user_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, role FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()
        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "role": row[2]
        }
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, email, role FROM users WHERE email = ?",
            (email,)
        )
        row = cur.fetchone()
        if not row:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "role": row[2]
        }
    finally:
        conn.close()
