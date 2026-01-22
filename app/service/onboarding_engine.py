from app.model.seating_db import allocate_seat
from app.service.email_service import (
    send_selected_with_seat_email,
    send_selected_no_seat_email,
    send_rejection_email
)
import re
from app.model.onboarding_db import save_employee
from app.model.find_model import get_employee_by_email

FIELDS = ["full_name", "email", "phone", "tech_stack", "tenth", "twelfth"]
TECH_STACKS = {"python", "java", "node", "qa"}
QUESTIONS = {
    "full_name": "May I have your full name?",
    "email": "Please share your email address.",
    "phone": "Enter your phone number.",
    "tech_stack": "Which tech stack are you skilled in?",
    "tenth": "What is your 10th percentage?",
    "twelfth": "What is your 12th percentage?"
}

def start_onboarding(session):
    session.update({
        "mode": "onboarding",
        "step": 0,
        "data": {},
        "paused": False
    })
    return QUESTIONS[FIELDS[0]]

def cancel_onboarding(session):
    session.clear()
    session["mode"] = "chat"
    return "No problem. I've stopped the onboarding process."

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

def handle_onboarding(session, message):
    field = FIELDS[session["step"]]

    if not validate(field, message):
        return f"That doesn’t look valid. {QUESTIONS[field]}"

    if field == "email":
        if get_employee_by_email(message.strip().lower()):
            session.clear()
            session["mode"] = "chat"
            return (
                "⚠️ Your response has already been submitted using this email.\n\n"
                "If you believe this is a mistake, please contact HR."
            )

    session["data"][field] = message.strip()
    session["step"] += 1

    if session["step"] < len(FIELDS):
        return QUESTIONS[FIELDS[session["step"]]]

    summary = session["data"]
    return (
        "Here’s a summary of your details:\n\n"
        f"Name: {summary['full_name']}\n"
        f"Email: {summary['email']}\n"
        f"Tech Stack: {summary['tech_stack']}\n"
        f"10th: {summary['tenth']}\n"
        f"12th: {summary['twelfth']}\n\n"
        "Type **confirm** to submit or **cancel** to exit."
    )

def eligible(data: dict) -> bool:
    return float(data["tenth"]) >= 70 and float(data["twelfth"]) >= 70


def finalize_onboarding(session: dict) -> str:
    data = session["data"]
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

    # Reset session AFTER commit
    session.clear()
    session["mode"] = "chat"

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
                f"Seat allocated: {seat_number}. "
                "Please check your email for onboarding details."
            )

        send_selected_no_seat_email(
            to_email=data["email"],
            name=data["full_name"],
            pdf_path=None
        )
        return (
            "✅ You meet the eligibility criteria.\n\n"
            "Seating is currently full. "
            "Seat details will be shared on your joining day."
        )

    send_rejection_email(
        to_email=data["email"],
        name=data["full_name"]
    )
    return (
        "Thank you for your interest.\n\n"
        "Unfortunately, you do not meet the eligibility criteria."
    )
