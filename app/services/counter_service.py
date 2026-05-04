from sqlalchemy.orm import Session

from app.models.votes import Vote
from app.services.administrator_service import AdministratorService
from app.services.commissioner_service import CommissionerService
from app.repositories.counted_votes_repository import save_counted_vote, get_tally,get_counted_vote_by_hash_n2
from app.models.counted_votes import CountedVoteStatus
from app.models.counted_votes import CountedVote
class CounterService:
    def __init__(self,db: Session = None,administrator_service : AdministratorService = None,commissioner_service: CommissionerService= None):
        self.administrator_service = administrator_service
        self.commissioner_service = commissioner_service
        self.db=db
    E = 65537
    N = 16790472354984960479090707660307983583745720096028900802657143315132855275087953358270654491644788077299207274681476412264395128440733567555676086977285682314016015753281334610688880002015512795100325174408920174908383115788076586545667677157078623303634548008429454467640797753945582051000437312512760701002384787545247587317653999473747541198854674490490213852483487477250829230142435892550191641519150211692377947144620327589348449609852721465449027949032724255153694805094209541038733374721333117074803950357458076873646278195946213692947195837284147639943262964772088807981380259482500880212335038885647343488947
    _D = 6721620347366913699580752951399060947299276934241943351976941453161200405834987019662006061351490913469063308643105652565248189416224207369741029005539880696255919393672110332270831068448036890493189057719951015592662761887422026101471492102066233745733799251554925727650395499832404453820703928026684006767044063143620236591272022041247244702001468014883621299869017323247775340906722235744566659919892175742329512951513830851162562127523030191971453129178202227752711406856406171663888275936016190551350218597844762780759101876030196646834908455825776291315206910333920061879395890532755685258099965568987598332801
    
    PUBLIC_KEY  = (E, N)
    _PRIVATE_KEY = (_D, N)
    
    def decrypt_all_votes(self,counter_prv_key: tuple[int, int], encrypted_votes_list: list[Vote]) -> list[int]:
        """
        Phase 1: Decrypt all ballots using counter's RSA private key.
        RSA decryption: m = c^d mod N
        """
        d, n = counter_prv_key
        decrypted_ballots = []
        
        for vote in encrypted_votes_list:
            encrypted = int(vote.encrypted_vote)
            decrypted = pow(encrypted, d, n) # m = c^d mod N
            decrypted_ballots.append(decrypted)
        
        return decrypted_ballots        
        
    def verify_signature(self, decrypted: int) -> tuple[bool, str, str]:
        """
        Check 1: Verify admin signature and extract ballot content.
        RSA verification: m = s^e mod N
        Returns (is_valid, vote, n2)
        """
        try:
            e, N = self.administrator_service.PUBLIC_KEY
            recovered_m = pow(decrypted, e, N)
            byte_length = (recovered_m.bit_length() + 7) // 8
            recovered_str = recovered_m.to_bytes(byte_length, byteorder='big').decode('utf-8')
            recovered_str = recovered_str.strip("()")
            parts = recovered_str.split(",")
            if len(parts) != 3:
                return False, "", ""
            vote, n2, _ = parts
            return True, vote, n2
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False, "", ""
        
    
    def is_n2_hash_exist(self,n2: str)->bool:
        return self.commissioner_service.is_n2_hash_exist(n2=n2)
    
    
    def process_all_votes(self, encrypted_votes_list: list[Vote]) -> dict:
        """
        Full counting protocol:
        Phase 1: Decrypt all ballots with counter's private key
        Phase 2: For each decrypted ballot:
            - Check 1: Verify administrator's signature
            - Check 2: Verify N2 fingerprint with commissioner
            - Save result to counted_votes table
        """
        results = {"valid": 0, "invalid_signature": 0, "invalid_n2": 0, "tally": {}}

        # Phase 1: Decrypt all votes
        decrypted_ballots = self.decrypt_all_votes(self._PRIVATE_KEY, encrypted_votes_list)

        # Phase 2: Verify each decrypted ballot
        for decrypted in decrypted_ballots:

            # Check 1: Verify admin signature
            is_valid, vote, n2 = self.verify_signature(decrypted)
            if not is_valid:
                save_counted_vote(db=self.db, n2="unknown", vote="unknown", status=CountedVoteStatus.INVALID_SIGNATURE)
                results["invalid_signature"] += 1
                continue

            # Check 2: Verify N2 fingerprint
            if not self.is_n2_hash_exist(n2):
                save_counted_vote(db=self.db, n2=n2, vote=vote, status=CountedVoteStatus.INVALID_N2)
                results["invalid_n2"] += 1
                continue

            # Valid vote - add to tally
            save_counted_vote(db=self.db, n2=n2, vote=vote, status=CountedVoteStatus.VALID)
            results["valid"] += 1
            results["tally"][vote] = results["tally"].get(vote, 0) + 1
            # Tally = the count of votes per candidate.

            # For example if 3 people voted "A" and 2 voted "B":

            # {
            # "valid": 5,
            # "invalid_signature": 0,
            # "invalid_n2": 0,
            # "tally": {
            # "A": 3,
            # "B": 2
            # }
            # }

        return results
    
    def get_results(self):
        return get_tally(db=self.db)
    
    def verify_vote_by_n2(self, n2: str) -> CountedVote | None:
        return get_counted_vote_by_hash_n2(db=self.db, n2=n2)