import os
from datetime import datetime, timedelta,timezone
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from app.pydantic.base_pydantic import TokenRequest, TokenPayload
from jose import jwt
from dotenv import load_dotenv

load_dotenv()
security = HTTPBasic()
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"
print(os.environ["JWT_SECRET_KEY"])
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

MAX_BCRYPT_BYTES = 72
def _normalize_password(password: str) -> bytes:
    if not isinstance(password, str):
        password = str(password)
    return password.encode("utf-8")[:MAX_BCRYPT_BYTES]

def create_access_token(subject: TokenRequest) -> str:
    expires_delta = datetime.now(tz=timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "exp": expires_delta,
        "email": subject.email,
        "id": subject.id,
        "token_type": "access_token"
    }

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: TokenRequest) -> str:
    expires_delta = datetime.now(tz=timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "exp": expires_delta,
        "email": subject.email,
        "id": subject.id,
        "token_type": "refresh_token"
    }

    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str, is_refresh: bool) -> dict | None:
    try:
        key = JWT_REFRESH_SECRET_KEY if is_refresh else JWT_SECRET_KEY

        decoded_token = jwt.decode(token, key, algorithms=[ALGORITHM])

        token_payload = TokenPayload(**decoded_token)

        # 🔑 UTC-safe expiry check
        if datetime.fromtimestamp(token_payload.exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
            return None

        return decoded_token

    except Exception as e:
        print("JWT decode error:", e)
        return None