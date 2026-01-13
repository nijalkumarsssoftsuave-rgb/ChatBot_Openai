from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["rag_chat_db"]
collection = db["chat_history"]

def save_chat(user_id:str,question: str, answer: str):
    collection.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "timestamp": datetime.now()
    })

def get_last_chats(user_id:str,limit: int = 10):
    # chats = collection.find().sort("timestamp", -1).limit(limit)
    chats = (
        collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return list(chats)[::-1]
