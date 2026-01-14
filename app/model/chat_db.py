from db.sqlite_db import get_connection

def save_chat(user_id: int, question: str, answer: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO chat_history (user_id, question, answer)
        VALUES (?, ?, ?)
        """,
        (user_id, question, answer)
    )

    conn.commit()
    conn.close()

def get_last_chats(user_id: int, limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT question, answer
        FROM chat_history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (user_id, limit)
    )

    rows = cur.fetchall()
    conn.close()

    # Oldest → newest
    return [{"question": q, "answer": a} for q, a in rows[::-1]]
