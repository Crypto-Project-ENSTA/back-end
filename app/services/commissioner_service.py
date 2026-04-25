from sqlalchemy.orm import Session
from app.repositories import credentials_repository

class CommissionerService: 
    def __init__(self, db: Session):
        self.db = db
    
    
    def is_n1_exist(self, voter_n1:str, removeN1 : bool = False)->bool:
        return credentials_repository.is_n1_exist(self.db,voter_n1,removeN1)