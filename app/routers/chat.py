from fastapi import APIRouter, Response, Depends
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.agent_service import generate_response
from app.services.auth_service import verify_token

router = APIRouter()

# Historial de conversación en memoria
conversation = []


@router.get("/", response_model=ChatResponse)
async def chat_welcome_endpoint():
    """
    return a welcome message just for the first GET request
    """

    return {"response": "Hi👋, Please Authenticate with userKey before I can help you"}


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user=Depends(verify_token)):
    """
    Endpoint to handle chat messages.
    """
    try:
        if not user:
            return Response(status_code=403, content="Invalid or missing token")

        global conversation
        conversation.append({"role": "user", "parts": [request.text]})
        reply = generate_response(request.text)
        conversation.append({"role": "model", "parts": [reply]})
        return {"response": reply}

    except Exception as e:
        return Response({"response": f"Error: {str(e)}"}, status_code=500)
