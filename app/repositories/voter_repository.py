from sqlalchemy.orm import Session
from app.schemas.voter import Voter as VoterSchema
from app.models.voter import Voter as VoterModel
from app.backend_config.voting_system_config import VotingSystemConfig
from app.models.credentials import Credential
from app.utils.crypto import hash_n2

def create_voter(db :Session , voter =VoterSchema ):
    db_voter = VoterModel(email=voter.email)
    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)
    return db_voter

# # this function is responsible for checking if the voters pool is full or not 
# def check_voter_limit(db: Session):
#     nbrs_of_lines= (db.query(VoterModel).count())
#     if ((nbrs_of_lines) == VotingSystemConfig.num_voters):
#         return True
#     return False

def save_voter_credentials(n1:str, n2: str , db : Session):
    hashed_n2 = hash_n2(n2)
    db_credential = Credential(n1 = n1,hash_n2 = hashed_n2)
    db.add(db_credential)
    db.commit()
    db.refresh(db_credential)
    return db_credential
