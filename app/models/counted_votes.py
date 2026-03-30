from sqlalchemy import Column, Integer, String
from app.database import Base


class CountedVote(Base):
    __tablename__ = "counted_votes"

    id = Column(Integer, primary_key=True, index=True)

    hash_n2 = Column(String, nullable=False, unique=True)

    vote = Column(String, nullable=False)

    status = Column(String, nullable=False)