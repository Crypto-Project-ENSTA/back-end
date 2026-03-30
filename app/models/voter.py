<<<<<<< HEAD
# ─────────────────────────────────────────────
# @sophia
# All models must inherit from Base (imported from app.database in the file app/database.py)
#
# Start every model like this:
#
#   from app.database import Base
#
#   class YourModel(Base): <-- this is the orm model name 
#       __tablename__ = "your_table" <-- this is the sql table name (same as excalidraw MCD)
#       ...
# ─────────────────────────────────────────────
=======
from sqlalchemy import Column, Integer, String
from app.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
>>>>>>> 8d22df4 ([03/30/2026 11:57:00] feat/models : implement all ORM models)
