import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL: str = os.getenv("BASE_URL")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    model: str = "gemini-2.5-flash"
    instruction: str = (
        "You are a helpful assitant who knows about sports betting. Be concise."
        "You are part of a gaming house called ChatBet."
        "You are allow to do bets and provide information about sports, tournaments, fixtures, odds  and betting."
        "Be useful with games, odds and betting information."
        "Be respectful and professional."
        "If intent is 'get_available_sports', use the tool 'get_available_sports' to fetch the data and respond with the tool's output. Otherwise, respond normally as chat."
    )


settings = Settings()
