from pydantic import BaseModel


class AuthenticateRequest(BaseModel):
    userkey: str


class TokenResponse(BaseModel):
    access_token: str
