
from sqlalchemy import Column, Integer, String
from app.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)