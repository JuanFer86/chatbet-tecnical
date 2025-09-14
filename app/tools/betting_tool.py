from langchain.tools import tool
import httpx
from app.core.config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import verify_token
from app.models.chat_models import PlaceBetBody

security = HTTPBearer()


@tool
def place_bet(
    body: PlaceBetBody, token: str, accept_language: str = "en"
) -> str | None:
    """
    place a bet
    arg:
        body (PlaceBetBody): user body request
        token (str): user token
        accept-language(str, optional): language
    Returns:
        str: A JSON string containing the status of the user and the userId
    """
    user = verify_token(token)
    body_parse = body.model_dump(by_alias=True)
    print("ahhh", body_parse)

    if user:
        with httpx.Client() as client:
            try:
                response = client.post(
                    f"{settings.BASE_URL}/place-bet",
                    headers={
                        "accept-language": accept_language,
                        "country-code": "BR",
                        "Token": token,
                    },
                    json=body_parse,
                )
                print("response", response)
                if response.status_code == 200:
                    return response.json()
                return None

            except httpx.RequestError as e:
                return None
    else:
        return "You must login to place a bet"


@tool
def get_user_balance(user_id: str, user_key: str, token: str) -> str | None:
    """
    place a bet
    arg:
        user_id(str): user id
        user_key(str): user key
        token (str): user token
    Returns:
        str: A JSON string containing the balance money from the user
    """
    user = verify_token(token)

    if user:
        with httpx.Client() as client:
            try:
                response = client.get(
                    f"{settings.BASE_URL}/auth/get_user_balance",
                    params={
                        "userId": user_id,
                        "userKey": user_key,
                    },
                    headers={
                        "Token": token,
                    },
                )

                if response.status_code == 200:
                    return response.json()
                return None

            except httpx.RequestError as e:
                return None
    else:
        return "You must login to get your balance"
