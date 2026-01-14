from fastapi import APIRouter
import re
from db.database import retrieve_context
from db.rag_openai import generate_answer
from app.model.onboarding_db import save_employee
from app.service.email_service import send_email
from db.sqlite_db import get_connection

router = APIRouter(prefix="/chatbot")

# --------------------
# In-memory chat state
# --------------------
sessions = {}

FIELDS = [
    "full_name",
    "email",
    "phone",
    "tech_stack",
    "tenth",
    "twelfth"
]

TECH_STACKS = {"python", "java", "node", "qa"}

QUESTIONS = {
    "full_name": "Please enter your full name.",
    "email": "Please enter your email address.",
    "phone": "Please enter your phone number.",
    "tech_stack": "Your tech stack? (python / java / node / qa)",
    "tenth": "Enter your 10th percentage.",
    "twelfth": "Enter your 12th percentage."
}

# --------------------
# Validators
# --------------------
def validate(field, value):
    if field == "full_name":
        return bool(value.strip())

    if field == "email":
        return re.match(r"[^@]+@[^@]+\.[^@]+", value)

    if field == "phone":
        return value.isdigit()

    if field == "tech_stack":
        return value.lower() in TECH_STACKS

    if field in ("tenth", "twelfth"):
        try:
            v = float(value)
            return 0 <= v <= 100
        except:
            return False

    return False

# --------------------
# Seat allocation (Matrix based)
# --------------------
def allocate_seat_matrix(tech_stack: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT row_number, column_number
        FROM seating
        WHERE tech_stack = ?
          AND employee_id IS NULL
        ORDER BY row_number, column_number
        LIMIT 1
    """, (tech_stack,))

    seat = cur.fetchone()
    conn.close()

    if not seat:
        return None

    row, col = seat
    return f"R{row}C{col}", row, col

# --------------------
# Chatbot endpoint
# --------------------
@router.post("/message")
def chatbot_message(message: str, session_id: str):
    msg = message.strip()

    # 🚀 Activate onboarding mode
    if msg.lower() == "i want to contact softsuave about onboarding":
        sessions[session_id] = {"step": 0, "data": {}}
        return {"reply": "Great! Let’s begin onboarding.\n" + QUESTIONS["full_name"]}

    # ❌ No active onboarding → RAG answer
    if session_id not in sessions:
        # normal RAG chat
        answer = generate_answer(msg, [])
        return {"reply": answer}

    # 🔄 Clear onboarding
    if msg.lower() == "clear":
        sessions.pop(session_id)
        return {"reply": "All onboarding data cleared. You can start again anytime."}

    session = sessions[session_id]
    step = session["step"]
    field = FIELDS[step]

    # ❌ Validation failed
    if not validate(field, msg):
        return {"reply": f"Invalid {field.replace('_', ' ')}. Please try again."}

    # ✅ Save input
    session["data"][field] = msg.strip().lower() if field == "tech_stack" else msg.strip()
    session["step"] += 1

    # ⏭ Ask next question
    if session["step"] < len(FIELDS):
        next_field = FIELDS[session["step"]]
        return {"reply": QUESTIONS[next_field]}

    # --------------------
    # 🎯 All data collected
    # --------------------
    data = session["data"]
    tenth = float(data["tenth"])
    twelfth = float(data["twelfth"])

    eligible = tenth >= 70 and twelfth >= 70

    seat_number = None
    if eligible:
        seat_info = allocate_seat_matrix(data["tech_stack"])
        if seat_info:
            seat_number, row, col = seat_info

            # Mark seat as occupied
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                UPDATE seating
                SET employee_id = ?
                WHERE row_number = ? AND column_number = ?
            """, (data["email"], row, col))
            conn.commit()
            conn.close()

    # Save employee
    save_employee({
        "name": data["full_name"],
        "email": data["email"],
        "phone": data["phone"],
        "tech_stack": data["tech_stack"],
        "tenth": tenth,
        "twelfth": twelfth,
        "status": "selected" if eligible else "rejected",
        "seat": seat_number
    })

    # Email
    if eligible:
        send_email(
            data["email"],
            "SoftSuave Onboarding Status",
            f"""
Hi {data['full_name']},

Congratulations! You are selected.

Tech Stack: {data['tech_stack'].capitalize()}
Seat Number: {seat_number or 'Will be assigned on joining day'}

Welcome to SoftSuave.
""",
            pdf_path=None
        )
        reply = "🎉 You are selected! Please check your email for onboarding details."
    else:
        send_email(
            data["email"],
            "SoftSuave Onboarding Update",
            f"""
Hi {data['full_name']},

Thank you for your interest in SoftSuave.

Unfortunately, you do not meet the onboarding criteria at this time.
We wish you the best ahead.
""",
            pdf_path=None
        )
        reply = "Thank you for your interest. Unfortunately, you are not eligible at this time."

    sessions.pop(session_id)
    return {"reply": reply}
