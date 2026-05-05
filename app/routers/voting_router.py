# app/routers/voting.py (or app/routers/status.py)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.voter_repository import get_all_voters
from app.repositories.voting_system_config_repo import emails_already_sent
from app.services.email_sender_service import send_email_to_voters

router = APIRouter(prefix="/voting")


@router.get("/is-started")
def is_voting_started(db: Session = Depends(get_db)):
    """
    Check if voting has started (emails have been sent to voters).
    """
    try:
        started = emails_already_sent(db)
        
        return {
            "voting_started": started,
            "message": "Voting has started" if started else "Voting has not started yet"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error checking voting status: {str(e)}"
        )

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
