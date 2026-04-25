from sqlalchemy.orm import Session
from app.models.votes import Vote, VoteStatus

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
        encrypted_vote=encrypted_vote,
        status=VoteStatus.VALID
    )
    
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    
    return new_vote