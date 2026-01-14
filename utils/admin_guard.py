from fastapi import Depends, HTTPException
from utils.JWT_Token import JWTBearer
from utils.jwt_utils import TokenPayload

def AdminOnly(user: TokenPayload = Depends(JWTBearer())):
    if getattr(user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
