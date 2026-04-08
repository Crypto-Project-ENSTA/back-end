from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_administrator_service
from app.schemas.n1_request import N1Request
from app.schemas.voter import Voter
from app.repositories import voter_repository
from app.services.administrator_service import AdministratorService

router = APIRouter(prefix="/voters",)

@router.post('/register')
def voter_register(voter : Voter, db:Session = Depends(get_db) ):
    try:
        created_voter = voter_repository.create_voter(db,voter)
        return {"status": "success", "voter": created_voter.email}
    except Exception as e:
        """
        - 400 Bad Request: If registration fails due to invalid input or other errors.
        (Indicates that the server could not process the request because the client
        sent incorrect or incomplete data.)
        """    
        raise HTTPException(status_code=400,detail=f"Error registering voter: {str(e)}")
    
    
@router.post('/check_n1')
def check_n1(voter_n1 : N1Request,service: AdministratorService = Depends(get_administrator_service)):
    try:
        result = service.request_commissioner_n1_exist(voter_n1.n1)
        if result:
            return {"is_N1_exist": True}
        else:
            return {"is_N1_exist": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))