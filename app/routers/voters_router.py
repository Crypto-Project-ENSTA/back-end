from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.voter import Voter
from app.repositories import voter_repository


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
    
    
