from sqlalchemy.orm import Session
from app.models.counted_votes import CountedVote, CountedVoteStatus


# Save a counted vote (valid or invalid) after counter verification.
def save_counted_vote(db: Session, hash_n2: str, vote: str, status: CountedVoteStatus):
    counted_vote = CountedVote(hash_n2=hash_n2, vote=vote, status=status)
    db.add(counted_vote)
    db.commit()
    db.refresh(counted_vote)
