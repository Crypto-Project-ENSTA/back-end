from app.database import SessionLocal
from app.models.voter import Voter
from app.models.votes import Vote

# create session
db = SessionLocal()

# create voter
<<<<<<< HEAD
new_voter = Voter(email="test3@test.com")
=======
new_voter = Voter(email="test@test.com")
>>>>>>> c1be64665d3bc2d0683ebb869238d656d33d50a4

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