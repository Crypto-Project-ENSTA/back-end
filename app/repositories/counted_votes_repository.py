from sqlalchemy.orm import Session
from app.models.counted_votes import CountedVote, CountedVoteStatus
from app.utils.crypto import hash_n2


# Save a counted vote (valid or invalid) after counter verification.
def save_counted_vote(db: Session, n2: str, vote: str, status: CountedVoteStatus) -> CountedVote:
    hash = hash_n2(n2) if n2 != "unknown" else "unknown"
    counted_vote = CountedVote(hash_n2=hash, vote=vote, status=status)
    db.add(counted_vote)
    db.commit()
    db.refresh(counted_vote)
    return counted_vote