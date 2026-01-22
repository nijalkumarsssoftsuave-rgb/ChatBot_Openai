from app.service.user_service import authenticate_user,verify_otp_and_create_user,user_exists
from utils.jwt_utils import create_access_token, create_refresh_token
from app.pydantic.base_pydantic import TokenRequest, TokenResponse
from fastapi import HTTPException,APIRouter
from app.service.otp_service import save_otp,generate_otp,verify_otp,delete_otp
from app.service.email_service import send_otp_email

auth_router = APIRouter()
@auth_router.post("/signup")
def signup(email: str, password: str):
    if user_exists(email):
        raise HTTPException(
            status_code=400,
            detail="User already registered. Please log in."
        )
    otp = generate_otp()
    save_otp(email, password, otp)
    send_otp_email(email=email, otp=otp)

    return {
        "message": "OTP sent to your email. Please verify to complete signup."
    }

@auth_router.post("/verify-otp")
def verify_user_otp(email: str, otp: str):
    return verify_otp_and_create_user(email=email, otp=otp)

@auth_router.post("/login", response_model=TokenResponse)
def login(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token_request = TokenRequest(
        id=str(user["id"]),
        email=user["email"],
        role=user["role"]
    )

    access_token = create_access_token(token_request)
    refresh_token = create_refresh_token(token_request)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
