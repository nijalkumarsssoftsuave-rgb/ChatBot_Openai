from fastapi import APIRouter, Request, Response, Depends
from utils.JWT_Token import JWTBearer
from app.pydantic.base_pydantic import TokenPayload
from app.service.session_service import get_or_create_session
from app.service.onboarding_service import handle_chatbot_message

onboarding_router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@onboarding_router.post("/message")
def chatbot(
    message: str,
    request: Request,
    response: Response,
    user: TokenPayload = Depends(JWTBearer())
):
    session = get_or_create_session(request, response)

    return handle_chatbot_message(
        user_id=int(user.id),
        message=message,
        session=session
    )
