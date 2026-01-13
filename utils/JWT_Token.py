from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.pydantic.base_pydantic import TokenPayload
from utils.jwt_utils import decode_jwt

def verify_jwt(token: str, is_refresh: bool) -> TokenPayload:
    payload = decode_jwt(token, is_refresh)
    if payload:
        return TokenPayload(**payload)
    return TokenPayload()


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            payload = verify_jwt(credentials.credentials,is_refresh=False)
            if payload.email is None:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return payload
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
