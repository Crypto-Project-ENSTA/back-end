# dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session               
from app.database import get_db
from app.services.administrator_service import AdministratorService
from app.services.commissioner_service import CommissionerService



def get_commissioner_service(db: Session = Depends(get_db)) -> CommissionerService:
    return CommissionerService(db)


def get_administrator_service(
    db: Session = Depends(get_db),
    commissioner: CommissionerService = Depends(get_commissioner_service)
) -> AdministratorService:
    return AdministratorService(db, commissioner)