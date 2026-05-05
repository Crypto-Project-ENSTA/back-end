from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.votes import Vote, VoteStatus
from app.models.voting_system_config_model import VotingConfigModel

def submit_encrypted_vote(db: Session, encrypted_vote: int) -> Vote:
    """
    Inserts the encrypted ballot into the ballot box (votes table).
    
    This function is called by the anonymizer after:
    1. N1 has been validated by the commissioner
    2. N1 has been marked as used (prevent double voting)
    
    The vote is stored encrypted — only the counter can
    decrypt it using his private key.

    """
    new_vote = Vote(
    encrypted_vote=str(encrypted_vote),
        status=VoteStatus.VALID
    )
    
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    return new_vote

def get_all_encrypted_votes(db: Session) -> list[Vote]:
    return db.query(Vote).filter(Vote.status == VoteStatus.VALID).all()

def has_reached_vote_limit(self) -> bool:
    # count only valid votes
    total_votes = (
        self.db.query(func.count(Vote.id))
        .filter(Vote.status == VoteStatus.VALID)
        .scalar()
    )

    # get total expected voters
    config = self.db.query(VotingConfigModel).first()
    total_voters = config.num_voters

    return total_votes >= total_voters