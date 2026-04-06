from sqlalchemy.orm import Session
from app.schemas.voter import Voter as VoterSchema
from app.models.voter import Voter as VoterModel

def create_voter(db :Session, voter =VoterSchema ):
    db_voter = VoterModel(email=voter.email)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter