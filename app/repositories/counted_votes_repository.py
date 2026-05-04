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

def get_tally(db: Session) -> dict:
    votes = db.query(CountedVote).filter(CountedVote.status == CountedVoteStatus.VALID).all()
    tally = {}
    for v in votes:
        tally[v.vote] = tally.get(v.vote, 0) + 1
    # {
    #   "A": 3,
    #   "B": 2
    # }
    return tally

# Fetch a single counted vote by n2 (used by voter to verify their vote was counted).
def get_counted_vote_by_hash_n2(db: Session, n2: str) -> CountedVote | None:
    hashed_n2 = hash_n2(n2)
    return db.query(CountedVote).filter(CountedVote.hash_n2 == hashed_n2).first()