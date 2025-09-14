import httpx
from fastapi import Depends, HTTPException
from app.models.auth_models import AuthenticateResponse
from app.core.config import settings


async def authenticate_user(userkey: str) -> AuthenticateResponse | None:
    """
    Call an external authentication service to validate user.
    """

    async with httpx.AsyncClient() as client:
        try:
            valid_user_key = await client.get(
                f"{settings.BASE_URL}/auth/validate_user",
                params={"userKey": userkey},
            )

            data = valid_user_key.json()

            if valid_user_key.status_code != 200:
                return None

            response = await client.post(
                f"{settings.BASE_URL}/auth/generate_token",
            )

            if response.status_code == 200:
                return_data = {
                    "token": response.json().get("token"),
                    "userKey": userkey,
                    "userId": data.get("userId"),
                }
                return return_data
            return None

        except httpx.RequestError as e:
            return None


def verify_token(token: str) -> bool:

    if not token:
        raise HTTPException(status_code=403, detail="token not sent")

    with httpx.Client() as client:
        try:
            response = client.get(
                f"{settings.BASE_URL}/auth/validate_token",
                headers={"token": token},
            )
            if response.status_code == 200:
                return True
        except httpx.RequestError as e:
            return False
