from app.service.intent_service import detect_intent
from app.service.onboarding_engine import (
    start_onboarding,
    handle_onboarding,
    finalize_onboarding,
    cancel_onboarding
)
from db.database import retrieve_context
from db.rag_openai import generate_answer
from app.model.chat_db import get_last_chats, save_chat


def handle_chatbot_message(
    *,
    user_id: int,
    message: str,
    session: dict
) -> dict:

    intent = detect_intent(message, session.get("mode"))

    # 1️⃣ Cancel onboarding
    if intent == "onboarding_cancel":
        reply = cancel_onboarding(session)
        save_chat(user_id, message, reply)
        return {"reply": reply}

    # 2️⃣ Start onboarding
    if intent == "onboarding_start" and session.get("mode") != "onboarding":
        reply = start_onboarding(session)
        save_chat(user_id, message, reply)
        return {"reply": reply}

    # 3️⃣ Continue onboarding
    if session.get("mode") == "onboarding":
        if message.lower() == "confirm":
            reply = finalize_onboarding(session)
            save_chat(user_id, message, reply)
            return {"reply": reply}

        reply = handle_onboarding(session, message)
        save_chat(user_id, message, reply)
        return {"reply": reply}

    # 4️⃣ Normal RAG chat
    history = get_last_chats(user_id)
    context = retrieve_context(message)
    answer = generate_answer(
        question=message,
        chat_history=history,
        context=context
    )

    save_chat(user_id, message, answer)
    return {"reply": answer}
