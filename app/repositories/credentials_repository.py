from sqlalchemy.orm import Session
from app.models.credentials import Credential as CredentialModel



# Check if N1 exists in the database (used by commissioner to verify voter identity).
def is_n1_exist(db:Session, voter_n1: str, removeN1 : bool = False) -> bool:
    db_cred = db.query(CredentialModel).filter(CredentialModel.n1 == voter_n1).first()
    if db_cred is None:
        return False
    
    #TODO : needs to handle this case so the voter knows that his N1 is already used 
    # If already used, reject the vote
    if db_cred.used:
        return False
    
    # Mark as used to prevent double voting
    if removeN1:
        db_cred.used = True
        db.commit()
    return True

# Check if N2 hash exists in the database (used by commissioner to verify ballot fingerprint).
def is_n2_hash_exist(db: Session, n2_hash: str) -> bool:
    db_cred = db.query(CredentialModel).filter(CredentialModel.hash_n2 == n2_hash).first()
    return db_cred is not None
