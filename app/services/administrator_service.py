from sqlalchemy.orm import Session

from app.services.commissioner_service import CommissionerService

class AdministratorService:
    
    def __init__(self, db: Session,commissioner : CommissionerService):
        self.db = db                                  
        self.commissioner = commissioner  
    
    def request_commissioner_n1_exist(self,voter_n1: str):
        return self.commissioner.is_n1_exist(voter_n1)