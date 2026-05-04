from fastapi import APIRouter,Depends,HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_administrator_service, get_anonymizer_service, get_counter_service, get_voting_system_service
from app.schemas.n1_request import N1Request
from app.schemas.vote_submission import VoteSubmission
from app.schemas.voter import Voter
from app.repositories import voter_repository
from app.services.administrator_service import AdministratorService
from app.services.anonymizer_service import AnonymizerService
from app.services.counter_service import CounterService
from app.services.voting_system_service import VotingSystemService

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
    

@router.post('/submit_vote')
def submit_vote(request: Request,vote_submission: VoteSubmission,voting_service: VotingSystemService = Depends(get_voting_system_service)
):
    try:
        n1 = request.session.get("n1")
        if not n1:
            raise HTTPException(status_code=403, detail="N1 not verified. Please verify your N1 first.")
        
        voting_service.submit_the_encrypted_ballot(
            n1=n1,
            n2=vote_submission.n2,
            vote=vote_submission.vote
        )
        
        request.session.pop("n1", None) 
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Vote submitted successfully and sent to anonymizer"
            }
        )
    
    except ValueError as ve:
        # Handle validation errors (e.g., invalid n2 format, invalid vote choice)
        raise HTTPException(
            status_code=400,
            detail=f"Invalid vote submission: {str(ve)}"
        )
    
    except Exception as e:
        # Handle any unexpected errors during the voting process
        raise HTTPException(
            status_code=500,
            detail=f"Error submitting vote: {str(e)}"
        )
        
        
@router.post('/end-vote')
def end_vote(
    counter_service: CounterService = Depends(get_counter_service),
    anonymizer_service: AnonymizerService = Depends(get_anonymizer_service)
):
    try:
        encrypted_votes = anonymizer_service.get_all_encrypted_votes()
        results = counter_service.process_all_votes(encrypted_votes_list=encrypted_votes)
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": "Votes counted successfully",
                "results": results
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting votes: {str(e)}")