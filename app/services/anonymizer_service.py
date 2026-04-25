from app.services.commissioner_service import CommissionerService

class AnonymizerService:
    def __init__(self, commissioner_service: CommissionerService):
        self.commissioner_service = commissioner_service
        
    def check_n1(self, voter_n1: str, removeN1: bool = True) -> bool:
        return self.commissioner_service.is_n1_exist(voter_n1, removeN1)
    
    