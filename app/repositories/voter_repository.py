from sqlalchemy.orm import Session
from app.schemas.voter import Voter

def create_voter(db :Session, voter =Voter ):
    db_voter = Voter(email=voter.email)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter