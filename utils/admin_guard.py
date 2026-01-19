from fastapi import Depends, HTTPException, status
from utils.JWT_Token import JWTBearer
from app.pydantic.base_pydantic import TokenPayload
from app.model.find_model import get_user_by_id

def admin_required(
    token: TokenPayload = Depends(JWTBearer())
):
    # 1️⃣ Fetch user from DB using token id
    user = get_user_by_id(int(token.id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # 2️⃣ Validate role from DB (NOT JWT)
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return user   # return DB user, not token
