from pydantic import BaseModel
from typing import List


class ChatResponse(BaseModel):
    response: str


class ChatRequest(BaseModel):
    text: str


class BetId(BaseModel):
    betId: str
    fixtureId: str
    odd: str
    sportId: str
    tournamentId: str


class User(BaseModel):
    userKey: str
    id: str


class BetInfo(BaseModel):
    amount: str
    betId: List[BetId]
    source: str


class PlaceBetBody(BaseModel):
    user: User
    betInfo: BetInfo
