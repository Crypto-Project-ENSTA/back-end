from app.database import Base, engine

# importer tous les models
from app.models.voter import Voter
from app.models.credentials import Credential
from app.models.votes import Vote
from app.models.counted_votes import CountedVote

def init_db():
    Base.metadata.create_all(bind=engine)