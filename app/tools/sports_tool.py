from langchain.tools import tool
import httpx
from app.core.config import settings


@tool
def get_available_sports() -> str:
    """
    Fetches a list of available sports
    Args:
        None
    Returns:
        str: A JSON string containing the list of available sports or an error message.
    """
    try:
        with httpx.Client() as client:
            response = client.get(f"{settings.BASE_URL}/sports")

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"
