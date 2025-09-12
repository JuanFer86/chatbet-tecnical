from langchain.tools import tool
import httpx
from app.core.config import settings


@tool(description="Get a list of available sports in the gaming house")
async def get_available_sports() -> str:
    """
    Fetches a list of available sports from an external API.
    """
    try:
        print("Fetching available sports...")
        async with httpx.Client() as client:
            response = await client.get(f"{settings.BASE_URL}/sports")

            if response.status_code == 200:
                return response.text
            return f"Error: Unable to fetch sports, status code {response.status_code}"
    except httpx.HTTPError as e:
        return f"Error fetching sports: {str(e)}"
