import uuid
import re
from fastapi import APIRouter, Request, Response, Depends, HTTPException
from utils.JWT_Token import JWTBearer
from app.pydantic.base_pydantic import TokenPayload
from db.database import retrieve_context
from db.rag_openai import generate_answer
from app.model.chat_db import save_chat, get_last_chats
from app.model.onboarding_db import save_employee
from app.model.seating_db import allocate_seat
from app.service.onboarding_service import (
    send_selected_with_seat_email,
    send_selected_no_seat_email,
    send_rejection_email
)
onboarding_router = APIRouter(prefix="/chatbot")

ONBOARDING_KEYWORDS = {
    "onboarding", "join", "apply", "job", "career", "hr", "recruitment"
}

FIELDS = ["full_name", "email", "phone", "tech_stack", "tenth", "twelfth"]

TECH_STACKS = {"python", "java", "node", "qa"}

QUESTIONS = {
    "full_name": "May I have your full name?",
    "email": "Please share your email address.",
    "phone": "Enter your phone number.",
    "tech_stack": "Which tech stack are you skilled in? (python / java / node / qa)",
    "tenth": "What is your 10th standard percentage?",
    "twelfth": "What is your 12th standard percentage?"
}
onboarding_sessions = {}

def generate_session_id() -> str:
    return str(uuid.uuid4())


def validate(field: str, value: str) -> bool:
    value = value.strip()

    if field == "full_name":
        return bool(re.fullmatch(r"[A-Za-z ]{2,}", value))

    if field == "email":
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value))

    if field == "phone":
        return bool(re.fullmatch(r"\d{10}", value))

    if field == "tech_stack":
        return value.lower() in TECH_STACKS

    if field in ("tenth", "twelfth"):
        try:
            v = float(value)
            return 0 <= v <= 100
        except ValueError:
            return False

    return False

def eligible(data: dict) -> bool:
    return float(data["tenth"]) >= 70 and float(data["twelfth"]) >= 70

def handle_onboarding(session_id: str, message: str) -> str:
    session = onboarding_sessions[session_id]
    field = FIELDS[session["step"]]

    if not validate(field, message):
        return f"That doesn’t seem valid. {QUESTIONS[field]}"

    session["data"][field] = (
        message.lower() if field == "tech_stack" else message.strip()
    )
    session["step"] += 1

    if session["step"] < len(FIELDS):
        return QUESTIONS[FIELDS[session["step"]]]

    summary = session["data"]
    return (
        "Thanks for sharing your details. Let me quickly verify eligibility.\n\n"
        f"• Name: {summary['full_name']}\n"
        f"• Email: {summary['email']}\n"
        f"• Tech Stack: {summary['tech_stack']}\n"
        f"• 10th %: {summary['tenth']}\n"
        f"• 12th %: {summary['twelfth']}\n\n"
        "Please type **confirm** to proceed."
    )

def finalize_onboarding(session_id: str) -> str:
    data = onboarding_sessions.pop(session_id)["data"]
    is_eligible = eligible(data)

    seat_number = None
    if is_eligible:
        seat_number = allocate_seat(
            tech_stack=data["tech_stack"],
            employee_email=data["email"]
        )

    save_employee({
        "name": data["full_name"],
        "email": data["email"],
        "phone": data["phone"],
        "tech_stack": data["tech_stack"],
        "tenth": float(data["tenth"]),
        "twelfth": float(data["twelfth"]),
        "status": "selected" if is_eligible else "rejected",
        "seat": seat_number
    })

    if is_eligible:
        if seat_number:
            send_selected_with_seat_email(
                to_email=data["email"],
                name=data["full_name"],
                seat_number=seat_number,
                tech_stack=data["tech_stack"],
                pdf_path=None
            )
            return (
                "✅ You meet the eligibility criteria.\n\n"
                f"Your seat has been allocated (Seat: {seat_number}). "
                "Please check your email for onboarding details."
            )

        send_selected_no_seat_email(
            to_email=data["email"],
            name=data["full_name"],
            pdf_path=None
        )
        return (
            "✅ You meet the eligibility criteria.\n\n"
            "Currently, seating is fully occupied. "
            "You will receive seat details on your joining day."
        )

    send_rejection_email(
        to_email=data["email"],
        name=data["full_name"]
    )
    return (
        "Thank you for your interest.\n\n"
        "At this time, you do not meet the eligibility criteria."
    )
@onboarding_router.post("/message")
def chatbot(
    message: str,
    request: Request,
    response: Response,
    user: TokenPayload = Depends(JWTBearer())
):
    user_id = int(user.id)
    msg = message.strip().lower()

    # session_id only for onboarding
    session_id = request.cookies.get("session_id")

    if not session_id:
        session_id = generate_session_id()
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            samesite="lax"
        )

    if msg == "clear all data":
        onboarding_sessions.pop(session_id, None)
        return {"reply": "All onboarding data has been cleared."}

    if session_id in onboarding_sessions:
        if msg == "confirm":
            reply = finalize_onboarding(session_id)
            save_chat(user_id, message, reply)
            return {"reply": reply}

        reply = handle_onboarding(session_id, message)
        save_chat(user_id, message, reply)
        return {"reply": reply}

    if any(k in msg for k in ONBOARDING_KEYWORDS):
        onboarding_sessions[session_id] = {"step": 0, "data": {}}
        reply = "Sure. I’ll help you with onboarding.\n\n" + QUESTIONS["full_name"]
        save_chat(user_id, message, reply)
        return {"reply": reply}

    try:
        history = get_last_chats(user_id, limit=20)
    except HTTPException:
        history = []

    context = retrieve_context(message)

    answer = generate_answer(
        question=message,
        chat_history=history,
        context=context
    )

    save_chat(user_id, message, answer)
    return {"reply": answer}
