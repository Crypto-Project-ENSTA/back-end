from fastapi import APIRouter,Depends,HTTPException, Request
from fastapi.responses import JSONResponse
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
        if voter_repository.check_email_existe(db=db, voter=voter):
            return JSONResponse(
                status_code=409,
                content={"status": "error", "message": "Email already exists", "voter": voter.email}
            )
        created_voter = voter_repository.create_voter(db,voter)
        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "Voter registered successfully", "voter": created_voter.email}
        )
    except Exception as e:
        """
        - 400 Bad Request: If registration fails due to invalid input or other errors.
        (Indicates that the server could not process the request because the client
        sent incorrect or incomplete data.)
        """    
        raise HTTPException(status_code=400,detail=f"Error registering voter: {str(e)}")
    
    
@router.post('/check_n1')
def check_n1(request : Request,voter_n1 : N1Request,service: AdministratorService = Depends(get_administrator_service)):
    try:
        result = service.request_commissioner_n1_exist(voter_n1.n1)
        if result:
            # Store the verified N1 code in the session so it can be retrieved
            # during the voting step without the voter needing to send it again.
            request.session["n1"] = voter_n1.n1
            return {"is_N1_exist": True}
        else:
            return {"is_N1_exist": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))