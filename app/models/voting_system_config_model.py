from sqlalchemy import Column, Boolean, Integer, String
from app.database import Base
from sqlalchemy.types import JSON

class VotingConfigModel(Base):
    __tablename__ = "voting_config"

    id = Column(Integer, primary_key=True)
    emails_sent = Column(Boolean, default=False)
    num_voters = Column(Integer, default=5)
    vote_theme = Column(String, nullable=True)
    choices = Column(JSON, nullable=True)