import uuid

sessions: dict[str, dict] = {}

SESSION_COOKIE = "chat_session_id"

def get_or_create_session(request, response):
    session_id = request.cookies.get(SESSION_COOKIE)

    if session_id and session_id in sessions:
        return sessions[session_id]

    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "mode": "chat",     # chat | onboarding
        "step": 0,
        "data": {},
        "paused": False
    }
    response.set_cookie(
        key=SESSION_COOKIE,
        value=session_id,
        httponly=True,
        samesite="lax"
    )

    return sessions[session_id]
