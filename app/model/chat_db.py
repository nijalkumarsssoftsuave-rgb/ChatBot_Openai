# from pymongo import MongoClient
# from datetime import datetime
#
# client = MongoClient("mongodb://localhost:27017")
# db = client["rag_chat_db"]
# collection = db["chat_history"]
#
# def save_chat(user_id:str,question: str, answer: str):
#     collection.insert_one({
#         "user_id": user_id,
#         "question": question,
#         "answer": answer,
#         "timestamp": datetime.now()
#     })
#
# def get_last_chats(user_id:str,limit: int = 10):
#     # chats = collection.find().sort("timestamp", -1).limit(limit)
#     chats = (
#         collection.find({"user_id": user_id})
#         .sort("timestamp", -1)
#         .limit(limit)
#     )
#     return list(chats)[::-1]


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
