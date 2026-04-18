
from app.services.administrator_service import AdministratorService
from app.dataclass.voter_ballot import (
    VoterBallotDTO,
    MaskedBallotDTO,
    SignedMaskedBallotDTO,
    SignedBallotDTO
)
from app.utils.crypto import (
    create_ballot,
    mask_ballot,
    unmask_signed_ballot
)
class VotingSystemService:

    def get_blind_signed_ballot(self,n2: str, vote: str):
        admin = AdministratorService(db=None, commissioner=None)
        ballot= create_ballot(n2=n2,vote=vote)
        print('the ballot:',ballot)
        masked_ballot = mask_ballot(voter_ballot=ballot,administrator_pub_key=AdministratorService.PUBLIC_KEY)
        print('the masked ballot ',masked_ballot)
        signed_masked_ballot = admin.sign_masked_ballot(masked_ballot)
        print('the signed masked ballot',signed_masked_ballot)
        unmask_sign_ballot = unmask_signed_ballot(admin_N_public_key=AdministratorService.PUBLIC_KEY[1],masked_Ballot=masked_ballot,signed_masked_ballot=signed_masked_ballot)
        print('the unmaks ballot: ',unmask_sign_ballot)