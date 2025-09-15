from fastapi import APIRouter, Response, Request, Header
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.agent_service import generate_response

router = APIRouter()

# memorized conversation
conversation = []


@router.get("/", response_model=ChatResponse)
async def chat_welcome_endpoint():
    """
    return a welcome message just for the first GET request and get sports and tournaments
    """

    return {"response": "Hi👋, How can I help you in your betting today?"}


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    Authorization: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
    x_user_key: str | None = Header(default=None),
):
    """
    Endpoint to handle chat messages.
    """
    try:
        # if not user:
        #     return Response(status_code=403, content="Invalid or missing token")
        user = None
        if Authorization and x_user_id and x_user_key:
            user = {
                "token": Authorization.replace("Bearer", "").strip(),
                "user_id": x_user_id,
                "user_key": x_user_key,
            }

        global conversation
        conversation.append({"role": "user", "parts": [chat_request.text]})
        reply = generate_response(chat_request.text, conversation, user)
        conversation.append({"role": "model", "parts": [reply]})

        return {"response": reply}

    except Exception as e:
        return Response({"response": f"Error: {str(e)}"}, status_code=500)
