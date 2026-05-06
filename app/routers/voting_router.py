# app/routers/voting.py (or app/routers/status.py)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_anonymizer_service, get_counter_service
from app.repositories.voter_repository import get_all_voters
from app.repositories.voting_system_config_repo import check_voting_status, emails_already_sent, set_voting_ended, set_voting_started
from app.schemas.vote_status_reponse import VoteStatusResponse
from app.services.anonymizer_service import AnonymizerService
from app.services.counter_service import CounterService
from app.services.email_sender_service import send_email_to_voters

router = APIRouter(prefix="/voting")


# @router.get("/is-started")
# def is_voting_started(db: Session = Depends(get_db)):
#     """
#     Check if voting has started (emails have been sent to voters).
#     """
#     try:
#         started = emails_already_sent(db)
        
#         return {
#             "voting_started": started,
#             "message": "Voting has started" if started else "Voting has not started yet"
#         }
    
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Error checking voting status: {str(e)}"
#         )

@router.post('/start-vote')
def start_vote(db: Session = Depends(get_db)):
    try:
        voters = get_all_voters(db=db)
        if not voters:
            raise HTTPException(status_code=404, detail="No voters found")
        
        send_email_to_voters(db=db, voters=voters)
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Voting started. Credentials sent to {len(voters)} voters."
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting vote: {str(e)}")

@router.post('/end-vote')
def end_vote(
    counter_service: CounterService = Depends(get_counter_service),
    anonymizer_service: AnonymizerService = Depends(get_anonymizer_service),
    db : Session= Depends(get_db)
):
    try:
        set_voting_ended(db=db)
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
    
    
    
@router.get("/vote-status", response_model=VoteStatusResponse)
def vote_status(db: Session = Depends(get_db)):
    status = check_voting_status(db)
    return VoteStatusResponse(
        voting_status=status,
    )