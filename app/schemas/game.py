from pydantic import BaseModel
from datetime import datetime

class GameStart(BaseModel):
    player1: str
    mode: str
    player2: str = None

class GamePlay(BaseModel):
    player: str
    choice: str

class GameResult(BaseModel):
    player1: str
    player2: str
    player1_score: int
    player2_score: int
    played_at: datetime

    class Config:
        from_attributes = True
