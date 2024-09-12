from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base
from datetime import datetime

class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)
    player1 = Column(String, index=True)
    player2 = Column(String, index=True)
    player1_score = Column(Integer)
    player2_score = Column(Integer)
    played_at = Column(DateTime, default=datetime.utcnow)
