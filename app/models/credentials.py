from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)

    n1 = Column(String, nullable=False, unique=True)
    hash_n2 = Column(String, nullable=False, unique=True)

    used = Column(Boolean, default=False, nullable=False)