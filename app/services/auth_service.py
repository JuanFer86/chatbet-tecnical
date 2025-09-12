import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings


async def authenticate_user(userkey: str) -> str | None:
    """
    Call an external authentication service to validate user.
    """

    async with httpx.AsyncClient() as client:
        try:
            valid_user_key = await client.get(
                f"{settings.BASE_URL}/auth/validate_user",
                params={"userKey": userkey},
            )

            if valid_user_key.status_code != 200:
                return None

            response = await client.post(
                f"{settings.BASE_URL}/auth/generate_token",
            )
            if response.status_code == 200:
                return response.json().get("token")
            return None

        except httpx.RequestError as e:
            return None


security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> bool:

    token = credentials.credentials

    if not token:
        raise HTTPException(status_code=403, detail="token not sent")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.BASE_URL}/auth/validate_token",
                headers={"token": token},
            )
            if response.status_code == 200:
                return True
        except httpx.RequestError as e:
            return False
