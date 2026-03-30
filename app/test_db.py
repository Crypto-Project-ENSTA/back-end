from app.database import SessionLocal
from app.models.voter import Voter
from app.models.votes import Vote

# create session
db = SessionLocal()

# create voter
new_voter = Voter(email="test@test.com")

# create vote
new_vote = Vote(
    encrypted_vote="encrypted123",
    status="pending"
)

# add to DB
db.add(new_voter)
db.add(new_vote)

# commit (save)
db.commit()

print("Data inserted successfully")

db.close()