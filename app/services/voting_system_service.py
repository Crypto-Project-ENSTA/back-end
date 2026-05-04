
from app.services.administrator_service import AdministratorService
from app.services.anonymizer_service import AnonymizerService
from app.services.counter_service import CounterService
from app.dataclass.voter_ballot import SignedBallotDTO,EncryptedSignedBallotDTO
from app.utils.crypto import (
    create_ballot,
    mask_ballot,
    unmask_signed_ballot,
    encrypt_signed_ballot
)
class VotingSystemService:
    def __init__(self,administrator_service: AdministratorService,anonymizer_service :AnonymizerService,counter_service :CounterService ):
        self.administrator_service = administrator_service
        self.anonymizer_service = anonymizer_service
        self.counter_service = counter_service
        
    def get_blind_signed_ballot(self,n2: str, vote: str)->SignedBallotDTO:
        """
        Execute the full RSA blind signature workflow for a voter.

        Steps:
        1. Create a ballot containing:
        - the vote
        - the nonce n2
        - random bits (for uniqueness)

        2. Convert and blind (mask) the ballot using the administrator's public key:
        m' = m * k^e mod N

        3. Send the masked ballot to the administrator for signing:
        s' = (m')^d mod N

        4. Unmask the signed ballot using the inverse of k:
        s = s' * k^{-1} mod N

        Result:
        - A valid RSA signature on the original ballot
        - The administrator never learns the original message (privacy preserved)
        """
        
        # Initialize administrator service (holds RSA keys)
        admin = self.administrator_service
        # Step 1: Create the ballot object
        ballot= create_ballot(n2=n2,vote=vote)
        print('the ballot:',ballot)
        # Step 2: Blind the ballot using public key (E, N)
        masked_ballot = mask_ballot(voter_ballot=ballot,administrator_pub_key=self.administrator_service.PUBLIC_KEY)
        print('the masked ballot ',masked_ballot)
        # Step 3: Administrator signs the masked ballot (blind signature)
        signed_masked_ballot = admin.sign_masked_ballot(masked_ballot)
        print('the signed masked ballot',signed_masked_ballot)
        # Step 4: Unmask the signature to obtain a valid signature on original ballot
        unmask_sign_ballot = unmask_signed_ballot(admin_N_public_key=self.administrator_service.PUBLIC_KEY[1],masked_Ballot=masked_ballot,signed_masked_ballot=signed_masked_ballot)
        print('the unmaks ballot: ',unmask_sign_ballot)
        
        return unmask_sign_ballot
    
    
    
    def get_encrypted_signed_ballot(self,signed_ballot: SignedBallotDTO, counter_public_key : tuple[int,int]) -> EncryptedSignedBallotDTO:
        """
        Encrypts a signed ballot using the vote counter's RSA public key.

        This step corresponds to "putting the ballot in an envelope" as described
        in the electronic voting protocol. The anonymizer will receive this encrypted
        ballot without being able to read its content, since only the counter holds
        the private key to decrypt it.

        RSA Encryption Formula:
            c = m^e mod N
        Where:
            - m : the signed ballot value
            - e : the counter's public exponent
            - N : the counter's RSA modulus
            - c : the resulting encrypted ballot
        """
        return encrypt_signed_ballot(signed_ballot, counter_public_key)
    
    
    def submit_the_encrypted_ballot(self,n1:str, n2: str, vote: str):
        """
        Complete workflow to submit an encrypted ballot.
        
        This method orchestrates the entire voting process:
        1. Get a blind-signed ballot from the administrator
        2. Encrypt the signed ballot with the counter's public key
        3. Submit the encrypted ballot (ready for anonymization and counting)

        """
        # Step 1: Execute blind signature protocol to get signed ballot
        signed_ballot = self.get_blind_signed_ballot(n2=n2, vote=vote)
        
        # Step 2: Encrypt the signed ballot with counter's public key
        encrypted_signed_ballot = self.get_encrypted_signed_ballot(
            signed_ballot=signed_ballot,
            counter_public_key=self.counter_service.PUBLIC_KEY  
        )
        
        print('Encrypted signed ballot ready for submission:', encrypted_signed_ballot)
        # Step 3: Submit to anonymizer (extracts just the encrypted vote value)
        self.anonymizer_service.anonymize_and_submit_vote(voter_n1=n1,
            encrypted_vote=encrypted_signed_ballot.encrypted_signed_ballot
        )
        
        print('Ballot submitted to anonymizer successfully')

    

        