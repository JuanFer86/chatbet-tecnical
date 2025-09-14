from fastapi import FastAPI
from app.routers import auth, chat

app = FastAPI()

# Registrar routers
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
