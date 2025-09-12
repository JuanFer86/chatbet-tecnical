from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage
from app.tools.sports_tool import get_available_sports
import json
import re
from app.core.config import settings

intent_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Classify the user's intent based on the input."
            "Answer just with JSON format {{'intent': 'intent'}}. "
            "Options: ['chat', 'get_available_sports'].",
        ),
        ("human", "{input}"),
    ]
)

main_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            settings.instruction,
        ),
        ("human", "{input}"),
    ]
)

chat = ChatGoogleGenerativeAI(
    api_key=settings.GEMINI_API_KEY,
    model=settings.model,
)

tools = [get_available_sports]

chat_with_tools = chat.bind_tools(tools)


def generate_response(user_input: str) -> str:
    intent_chain = intent_prompt | chat

    # step 1 - get the intent
    try:
        intent_raw = intent_chain.invoke({"input": user_input})

        cleaned = re.sub(
            r"^```json\n?|```$", "", intent_raw.content.strip(), flags=re.MULTILINE
        ).strip()

        intent = json.loads(cleaned)["intent"]

    except Exception as e:
        intent = "chat"

    # step 2 - after getting the intent, call the main chain
    if intent == "get_available_sports":
        chain = main_prompt | chat_with_tools
    else:
        chain = main_prompt | chat

    # step 3 - get the final response
    response = chain.invoke({"input": user_input, "intent": intent})

    return response.content
