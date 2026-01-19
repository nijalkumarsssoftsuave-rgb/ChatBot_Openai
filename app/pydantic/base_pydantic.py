from pydantic import BaseModel, Field

class TokenRequest(BaseModel):
    id: str
    email: str
    role: str


class TokenPayload(BaseModel):
    exp: int = None
    email: str = None
    id: str = None
    token_type: str = None


class TokenResponse(BaseModel):
    access_token: str = Field(..., examples=["eyJQGdtYWlsLmNvbSIsImlkIjoiNzBjMzhkYTEtNmEzYS00NDQ2LTg5MGMtNDYzOTM4YzA0NmFhIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiJ9.IJI-K-BsqODkgjI8MN-NBxBKmIxQ6z_ZOLhmKWMouTc"])
    refresh_token: str = Field(..., examples=["eyJQGdtYWlsLmNvbSIsImlkIjoiNzBjMzhkYTEtNmEzYS00NDQ2LTg5MGMtNDYzOTM4YzA0NmFhIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiJ9.IJI-K-BsqODkgjI8MN-NBxBKmIxQ6z_ZOLhmKWMouTc"])
