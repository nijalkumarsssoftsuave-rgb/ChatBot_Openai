from fastapi import APIRouter, HTTPException
from app.model.auth_model import create_user, authenticate_user
from utils.jwt_utils import create_access_token, create_refresh_token
from app.pydantic.base_pydantic import TokenRequest, TokenResponse

admin_auth_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_auth_router.post("/signup")
def admin_signup(email: str, password: str):
    admin = create_user(email, password, role="admin")
    if not admin:
        raise HTTPException(400, "Admin already exists")

    return {"message": "Admin signup successful"}

@admin_auth_router.post("/login", response_model=TokenResponse)
def admin_login(email: str, password: str):
    admin = authenticate_user(email, password)

    if not admin or admin["role"] != "admin":
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    token_request = TokenRequest(
        id=str(admin["id"]),
        email=admin["email"],
        role=admin["role"]
    )

    return {
        "access_token": create_access_token(token_request),
        "refresh_token": create_refresh_token(token_request)
    }
