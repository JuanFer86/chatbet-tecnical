from langchain.tools import tool
import httpx
from app.core.config import settings


@tool
def get_odds(sport_id: int, tournament_id: int, fixture_id: int, amount: int) -> str:
    """
    Fetch odds from a fixture
    Args:
        sportId (int): Sport ID
        tournamentId (int): Tournament ID
        fixtureId (int): Fixture ID
        amount (int): Number of odds to fetch
    Returns:
        str: A JSON string containing the odds or an error message.
    """
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{settings.BASE_URL}/sports/odds",
                params={
                    "sportId": sport_id,
                    "tournamentId": tournament_id,
                    "fixtureId": fixture_id,
                    "amount": amount,
                },
            )

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"
