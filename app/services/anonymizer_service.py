from sqlalchemy.orm import Session

from app.services.commissioner_service import CommissionerService
from app.repositories.votes_repository import submit_encrypted_vote,get_all_encrypted_votes
class AnonymizerService:
    def __init__(self, db:Session,commissioner_service: CommissionerService):
        self.db = db
        self.commissioner_service = commissioner_service
        
        
    def check_n1(self, voter_n1: str, removeN1: bool = True) -> bool:
        return self.commissioner_service.is_n1_exist(voter_n1=voter_n1, removeN1=removeN1)
    
    def submit_encrypted_ballot(self,encrypted_vote:int):
        return submit_encrypted_vote(db=self.db,encrypted_vote=encrypted_vote)
    
    def anonymize_and_submit_vote(self, voter_n1: str, encrypted_vote: int) -> bool:
        if not self.check_n1(voter_n1=voter_n1, removeN1=True):
            return False
        self.submit_encrypted_ballot(encrypted_vote=encrypted_vote)
        return True
    
    def get_all_encrypted_votes(self):
        return get_all_encrypted_votes(db=self.db)