from sqlalchemy.orm import Session
from app.repositories import credentials_repository
from app.utils.crypto import hash_n2
class CommissionerService: 
    def __init__(self, db: Session):
        self.db = db
    
    
    def is_n1_exist(self, voter_n1:str, removeN1 : bool = False)->bool:
        return credentials_repository.is_n1_exist(self.db,voter_n1,removeN1)
    
    def is_n2_hash_exist(self, n2: str) -> bool:
        n2_hash = hash_n2(n2)
        return credentials_repository.is_n2_hash_exist(db=self.db,n2_hash=n2_hash)
