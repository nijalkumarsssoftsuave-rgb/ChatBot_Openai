from fastapi import APIRouter
import re
from db.rag_openai import generate_answer
from app.model.onboarding_db import save_employee


onboarding_router = APIRouter(prefix="/chatbot")

# --------------------
# Onboarding intent
# --------------------
ONBOARDING_KEYWORDS = {
    "onboarding", "join", "apply", "job", "career", "hr", "recruitment"
}

# --------------------
# Session store
# --------------------
onboarding_sessions = {}

# --------------------
# Fields & questions
# --------------------
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

# --------------------
# Validation
# --------------------
def validate(field, value):
    if field == "full_name":
        return bool(value.strip())

    if field == "email":
        return re.match(r"^[^@]+@[^@]+\.[^@]+$", value)

    if field == "phone":
        return value.isdigit() and len(value) >= 10

    if field == "tech_stack":
        return value.lower() in TECH_STACKS

    if field in ("tenth", "twelfth"):
        try:
            v = float(value)
            return 0 <= v <= 100
        except ValueError:
            return False

    return False

def eligible(data):
    return float(data["tenth"]) > 70 and float(data["twelfth"]) > 70

# --------------------
# Onboarding flow
# --------------------
def handle_onboarding(session_id, message):
    session = onboarding_sessions[session_id]
    field = FIELDS[session["step"]]

    if not validate(field, message):
        return {"reply": f"That doesn’t seem valid. {QUESTIONS[field]}"}

    session["data"][field] = (
        message.lower() if field == "tech_stack" else message.strip()
    )
    session["step"] += 1

    if session["step"] < len(FIELDS):
        return {"reply": QUESTIONS[FIELDS[session["step"]]]}

    summary = session["data"]
    return {
        "reply": (
            "Thanks for sharing your details. Let me quickly verify eligibility.\n\n"
            f"• Name: {summary['full_name']}\n"
            f"• Email: {summary['email']}\n"
            f"• Tech Stack: {summary['tech_stack']}\n"
            f"• 10th %: {summary['tenth']}\n"
            f"• 12th %: {summary['twelfth']}\n\n"
            "Please type **confirm** to proceed."
        )
    }

def finalize_onboarding(session_id):
    session = onboarding_sessions.pop(session_id)
    data = session["data"]

    is_eligible = float(data["tenth"]) > 70 and float(data["twelfth"]) > 70

    employee_payload = {
        "name": data["full_name"],
        "email": data["email"],
        "phone": data["phone"],
        "tech_stack": data["tech_stack"],
        "tenth": float(data["tenth"]),
        "twelfth": float(data["twelfth"]),
        "status": "selected" if is_eligible else "rejected",
        "seat": None   # seating can be added later
    }

    # ✅ SAVE TO DB
    save_employee(employee_payload)

    if is_eligible:
        return {
            "reply": (
                "✅ You meet the eligibility criteria.\n\n"
                "Your details have been successfully recorded. "
                "Our HR team will guide you through the next steps."
            )
        }

    return {
        "reply": (
            "Thank you for your interest.\n\n"
            "Your details have been recorded. "
            "At this time, you do not meet the eligibility criteria. "
            "We encourage you to reapply in the future."
        )
    }


# --------------------
# Chatbot endpoint
# --------------------
@onboarding_router.post("/message")
def chatbot(message: str, session_id: str):
    msg = message.strip().lower()

    if msg == "clear all data":
        onboarding_sessions.pop(session_id, None)
        return {"reply": "All onboarding data has been cleared."}

    if session_id in onboarding_sessions:
        if msg == "confirm":
            return finalize_onboarding(session_id)
        return handle_onboarding(session_id, message)

    if any(k in msg for k in ONBOARDING_KEYWORDS):
        onboarding_sessions[session_id] = {"step": 0, "data": {}}
        return {"reply": "Sure. I’ll help you with onboarding.\n\n" + QUESTIONS["full_name"]}

    answer = generate_answer(message, [])
    return {"reply": answer}
