# dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session               
from app.database import get_db
from app.services.administrator_service import AdministratorService



def get_administrator_service(db: Session = Depends(get_db)) -> AdministratorService:
    return AdministratorService(db)