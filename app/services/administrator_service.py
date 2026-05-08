from sqlalchemy.orm import Session

from app.services.commissioner_service import CommissionerService
from app.utils.crypto import sign_masked_ballot
from app.dataclass.voter_ballot import MaskedBallotDTO
from app.key_loader import admin_private_key, admin_public_key

class AdministratorService:
        
    def __init__(self, db: Session,commissioner : CommissionerService):
        self.db = db                                  
        self.commissioner = commissioner
        self._private_key = admin_private_key
        self._public_key = admin_public_key
    
    @property
    def PUBLIC_KEY(self) -> tuple[int, int]:
        pub_numbers = self._public_key.public_numbers()
        return (pub_numbers.e, pub_numbers.n)
    @property
    def _PRIVATE_KEY(self) -> tuple[int, int]:
        priv_numbers = self._private_key.private_numbers()
        return (priv_numbers.d, priv_numbers.public_numbers.n)
    
    def request_commissioner_n1_exist(self,voter_n1: str):
        return self.commissioner.is_n1_exist(voter_n1)
    
    def sign_masked_ballot(self, masked_ballot: MaskedBallotDTO):
        return sign_masked_ballot(
            admin_N_public_key=self._PRIVATE_KEY[1],
            admin_private_key=self._PRIVATE_KEY[0],
            masked_ballot=masked_ballot
        )