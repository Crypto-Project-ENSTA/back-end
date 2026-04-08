from sqlalchemy import Column, Boolean, Integer, String
from app.database import Base
from sqlalchemy.types import JSON

class VotingConfigModel(Base):
    __tablename__ = "voting_config"

    id = Column(Integer, primary_key=True)
    emails_sent = Column(Boolean, default=False)
    num_voters = Column(Integer, default=5)
    vote_theme = Column(String, nullable=True)
    # JSON type allows storing a list of strings directly in the DB as a JSON array
    # example stored value: ["option1", "option2", "option3"]
    # we use default=[] so if no choices are provided the column is not NULL
    # but an empty list instead, avoiding NoneType errors when iterating over it
    choices = Column(JSON, nullable=True, default=[])  