from app.model.auth_model import create_user, authenticate_user
from utils.jwt_utils import create_access_token, create_refresh_token
from app.pydantic.base_pydantic import TokenRequest, TokenResponse
from fastapi import HTTPException,APIRouter

auth_router = APIRouter()

@auth_router.post("/signup")
def signup(email: str, password: str):
    user = create_user(email, password)
    if not user:
        raise HTTPException(400, "User already exists")

    return {"message": "Signup successful"}

# @auth_router.post("/login", response_model=TokenResponse)
@auth_router.post("/login", response_model=TokenResponse)
def login(email: str, password: str):
    user = authenticate_user(email, password)
    # print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_request = TokenRequest(
        id=str(user["id"]),        # ✅ FIXED
        email=user["email"]
    )

    access_token = create_access_token(token_request)
    refresh_token = create_refresh_token(token_request)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
