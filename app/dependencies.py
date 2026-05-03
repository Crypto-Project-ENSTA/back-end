# dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session               
from app.database import get_db
from app.services.administrator_service import AdministratorService
from app.services.commissioner_service import CommissionerService
from app.services.voting_system_service import VotingSystemService
from app.services.anonymizer_service import AnonymizerService
from app.services.counter_service import CounterSerivce




def get_commissioner_service(db: Session = Depends(get_db)) -> CommissionerService:
    return CommissionerService(db)


def get_administrator_service(
    db: Session = Depends(get_db),
    commissioner: CommissionerService = Depends(get_commissioner_service)
) -> AdministratorService:
    return AdministratorService(db, commissioner)


def get_anonymizer_service(db :Session =Depends(get_db),commissioner: CommissionerService = Depends(get_commissioner_service)
) -> AnonymizerService:
    return AnonymizerService(db=db,commissioner_service=commissioner)


def get_counter_service(
    administrator_service: AdministratorService = Depends(get_administrator_service),
    commissioner_service: CommissionerService = Depends(get_commissioner_service),
    db: Session = Depends(get_db)
) -> CounterSerivce:
    return CounterSerivce(
        administrator_service=administrator_service,
        commissioner_service=commissioner_service,
        db=db
    )
    
def get_voting_system_service(
    administrator_service: AdministratorService = Depends(get_administrator_service),
    anonymizer_service: AnonymizerService = Depends(get_anonymizer_service),
    counter_service: CounterSerivce = Depends(get_counter_service)
) -> VotingSystemService:

    return VotingSystemService(
        administrator_service=administrator_service,
        anonymizer_service=anonymizer_service,
        counter_service=counter_service
    )
