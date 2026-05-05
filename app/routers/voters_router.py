from fastapi import APIRouter,Depends,HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_administrator_service, get_anonymizer_service, get_counter_service, get_voting_system_service
from app.schemas.n1_check_response import N1CheckResponse
from app.schemas.n1_request import N1Request
from app.schemas.register_response import RegisterResponse
from app.schemas.vote_submission import VoteSubmission
from app.schemas.vote_submission_response import SubmitVoteResponse
from app.schemas.voter import Voter
from app.repositories import voter_repository
from app.services.administrator_service import AdministratorService
from app.services.anonymizer_service import AnonymizerService
from app.services.counter_service import CounterService
from app.services.voting_system_service import VotingSystemService

router = APIRouter(prefix="/voters",)

@router.post('/register',response_model=RegisterResponse,
    status_code=201,
    summary="Register a new voter",
    description="""
    Registers a voter by their email address.

    - Returns **201** on success.
    - Returns **409** if the email is already registered — the response body
    still follows the standard `RegisterResponse` shape with `status: "error"`.
    - Returns **400** for any other failure (e.g. malformed payload, DB error).
    """,
        responses={
            201: {"description": "Voter registered successfully"},
            409: {"description": "Email already exists in the system"},
            400: {"description": "Registration failed due to invalid input or unexpected error"}
        }
)
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
    
    
@router.post('/check_n1',
    response_model=N1CheckResponse,
    summary="Validate a voter's N1 code",
    description="""
Verifies that the supplied **N1 code** is recognised by the commissioner.

If valid, the code is stored server-side in the caller's **session** so it
can be retrieved transparently during the subsequent `/submit_vote` call —
the voter does **not** need to resend it.

> This step must be completed before calling `/submit_vote`,
> otherwise that endpoint will return **403**.
""",
    responses={
        200: {"description": "Check completed — inspect `is_N1_exist` in the response"},
        500: {"description": "Unexpected error communicating with the commissioner service"}
    }
)
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
    

@router.post('/submit_vote',
    response_model=SubmitVoteResponse,
    summary="Submit an encrypted ballot",
    description="""
Submits the voter's encrypted ballot to the anonymizer pipeline.

**Prerequisites:**
- `/check_n1` must have been called first in the same session. The N1 code
  is read from the session automatically and cleared once the vote is
  accepted, preventing double voting.

**Payload fields:**
- `n2` — the voter's unique second-factor fingerprint.
- `vote` — the encrypted vote choice.

**Error cases:**
| Code | Reason |
|------|--------|
| 403  | N1 not present in session (step skipped or session expired) |
| 400  | Malformed `n2`, unrecognised vote value, or other validation failure |
| 500  | Unexpected server-side error during ballot processing |
""",
    responses={
        200: {"description": "Ballot accepted and forwarded to the anonymizer"},
        403: {"description": "N1 not verified — call `/check_n1` first"},
        400: {"description": "Invalid `n2` format or unrecognised vote choice"},
        500: {"description": "Unexpected error during vote submission"}
    })
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