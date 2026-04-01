from sqlalchemy import Column, Integer, String, Enum
import enum
from app.database import Base


class CountedVoteStatus(enum.Enum):
    VALID = "valid"
    INVALID_SIGNATURE = "invalid_signature"
    INVALID_N2 = "invalid_n2"


class CountedVote(Base):
    __tablename__ = "counted_votes"

    id = Column(Integer, primary_key=True, index=True)

    hash_n2 = Column(String, nullable=False, unique=True)

    vote = Column(String, nullable=False)

    status = Column(Enum(CountedVoteStatus), nullable=False)