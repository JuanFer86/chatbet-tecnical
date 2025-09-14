from langchain.tools import tool
import httpx
from app.core.config import settings


@tool
def get_fixtures(
    tournament_id: int,
    lang: str = "en",
    time_zone: str = "UTC",
) -> str:
    """
    Fetch a list of fixtures(matches / games) by tournament
    Args:
        tournamentId (int): Tournament ID
        lang (str, optional): Language code. Defaults to "en".
        time_zone (str, optional): Time zone. Defaults to "UTC".
    Returns:
        str: A JSON string containing the list of fixtures or an error message.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.BASE_URL}/sports/fixtures",
                params={
                    "tournamentId": tournament_id,
                    "type": "pre_match",
                    "language": lang,
                    "time_zone": time_zone,
                },
            )

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"


@tool
def get_sports_fixtures(sport_id: int, lang: str = "en", time_zone: str = "UTC") -> str:
    """
    Fetch a list of fixtures(matches / games) by sport
    Args:
        sportId (int): Sport ID
        lang (str, optional): Language code. Defaults to "en".
        time_zone (str, optional): Time zone. Defaults to "UTC".
    Returns:
        str: A JSON string containing the list of fixtures or an error message.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.BASE_URL}/sports/sports-fixtures",
                params={
                    "sportId": sport_id,
                    "type": "pre_match",
                    "language": lang,
                    "time_zone": time_zone,
                },
            )

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"
