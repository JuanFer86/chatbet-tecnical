from pydantic import BaseModel


class AuthenticateRequest(BaseModel):
    userkey: str


class AuthenticateResponse(BaseModel):
    token: str
    userKey: str
    userId: str


class TokenResponse(BaseModel):
    access_token: str
