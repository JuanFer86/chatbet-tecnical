from langchain.tools import tool
import httpx
from app.core.config import settings


@tool
def get_available_tournaments(id: int, lang: str = "en") -> str:
    """
    Fetches a list of available torunaments by sport.
    Args:
        id (int): Sport ID
        lang (str, optional): Language code. Defaults to "en".
    Returns:
        str: A JSON string containing the list of available tournaments or an error message.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.BASE_URL}/sports/tournaments",
                params={"id": id, "language": lang},
            )

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"


@tool
def get_available_all_tournaments(
    lang: str = "en", active_fixtures: bool = True
) -> str:
    """
    Fetches a list of available sports.
    Args:
        lang (str, optional): Language code. Defaults to "en".
        active_fixtures (bool, optional): Whether to include only tournaments with active fixtures. Defaults to True.
    Returns:
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.BASE_URL}/sports/all-tournaments",
                params={"lang": lang, "with_active_fixtures": active_fixtures},
            )

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"
