# app/routers/voting.py (or app/routers/status.py)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.voting_system_config_repo import emails_already_sent

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

