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