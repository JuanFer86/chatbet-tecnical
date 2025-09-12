from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models.auth_models import AuthenticateRequest
from app.services.auth_service import authenticate_user

router = APIRouter()

# Historial de conversación en memoria


@router.post("/")
async def auth_endpoint(request: AuthenticateRequest):

    try:
        reply = await authenticate_user(request.userkey)
        return {"token": reply}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
