from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_vote = Column(String, nullable=False)

    submitted_at = Column(DateTime, default=datetime.utcnow)

    status = Column(String, default="pending")