from sqlalchemy.orm import Session
from app.models.credentials import Credential as CredentialModel



# Check if N1 exists in the database (used by commissioner to verify voter identity).
def is_n1_exist(db:Session, voter_n1: str, removeN1 : bool = False) -> bool:
    db_cred = db.query(CredentialModel).filter(CredentialModel.n1 == voter_n1).first()
    if db_cred is None:
        return False
    
    # If already used, reject the vote
    if db_cred.used:
        return False
    
    # Mark as used to prevent double voting
    if removeN1:
        db_cred.used = True
        db.commit()
    return True