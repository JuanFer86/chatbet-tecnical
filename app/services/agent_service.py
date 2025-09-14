from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, ToolMessage
from app.tools.sports_tool import get_available_sports
from app.tools.tournaments_tool import (
    get_available_tournaments,
    get_available_all_tournaments,
)
from app.tools.odds_tool import get_odds
from app.tools.fixtures_tool import get_fixtures, get_sports_fixtures
from app.tools.betting_tool import place_bet, get_user_balance
from app.utils.build_messages import build_messages_from_history
from app.models.auth_models import AuthenticateResponse
from app.core.config import settings

intent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            settings.instruction_intent,
        ),
        ("human", "{input}"),
    ]
)


main_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            settings.main_instruction,
        ),
        ("human", "{input}"),
    ]
)

chat = ChatGoogleGenerativeAI(
    api_key=settings.GEMINI_API_KEY,
    model=settings.model,
)

tools = [
    get_available_sports,
    get_available_tournaments,
    get_available_all_tournaments,
    get_fixtures,
    get_sports_fixtures,
    get_odds,
    place_bet,
    get_user_balance,
]


chat_with_tools = chat.bind_tools(tools)


def generate_response(
    user_input: str, conversation_history=None, user: AuthenticateResponse = None
) -> str:

    tool_calls = []

    try:
        if conversation_history:
            messages = build_messages_from_history(conversation_history)

        if user:
            messages.insert(0, HumanMessage(content=f"{user}"))

        messages.append(HumanMessage(user_input))

        while True:
            intents_chain = intent_prompt | chat_with_tools
            intent_tool_calls = intents_chain.invoke(messages)

            print("intent_tool_calls", intent_tool_calls.tool_calls)

            tool_calls_aux = [tool["name"] for tool in intent_tool_calls.tool_calls]

            if not intent_tool_calls.tool_calls or all(
                name in tool_calls for name in tool_calls_aux
            ):
                break

            for tool_call in intent_tool_calls.tool_calls:
                if any(tool != tool_call["name"] for tool in tool_calls):
                    tool_calls.extend(tool_call["name"])
                    continue

                selected_tool = {
                    "get_available_sports": get_available_sports,
                    "get_available_tournaments": get_available_tournaments,
                    "get_available_all_tournaments": get_available_all_tournaments,
                    "get_fixtures": get_fixtures,
                    "get_sports_fixtures": get_sports_fixtures,
                    "get_odds": get_odds,
                    "place_bet": place_bet,
                    "get_user_balance": get_user_balance,
                }

                tool = selected_tool[tool_call["name"].lower()]
                tool_msg = tool.invoke(tool_call)
                tool_result_msg = ToolMessage(
                    tool_call_id=tool_call["id"], content=str(tool_msg)
                )
                messages.append(tool_result_msg)

        # print(messages)
        chat_chain = main_prompt | chat_with_tools
        response = chat_chain.invoke(messages)

        return response.content
    except Exception as e:
        return f"Error generating response: {str(e)}"
