from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
from datetime import datetime
from app.database import Base


class VoteStatus(enum.Enum):
    VALID = "valid"
    REJECTED = "rejected"


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)

    encrypted_vote = Column(String, nullable=False)

    submitted_at = Column(DateTime, default=datetime.utcnow)

    status = Column(Enum(VoteStatus), default=VoteStatus.PENDING, nullable=False)