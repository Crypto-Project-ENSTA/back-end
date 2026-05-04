from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.verify_vote_request import VerifyVoteRequest
from app.services.counter_service import CounterService
from app.dependencies import get_counter_service

router = APIRouter(prefix="/results")



@router.get("/tally")
def get_election_results(
    counter_service: CounterService = Depends(get_counter_service)
):
    """
    Get the current election results tally.
    
    Returns:
        dict: Vote counts per candidate
        Example: {"A": 3, "B": 2}
    """
    try:
        results = counter_service.get_results()
        
        if not results:
            return {
                "message": "No valid votes counted yet",
                "tally": {}
            }
        
        # Calculate total valid votes
        total_votes = sum(results.values())
        
        return {
            "total_votes": total_votes,
            "tally": results
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving results: {str(e)}"
        )

@router.post("/verify-vote")
def verify_my_vote(
    request: VerifyVoteRequest,
    counter_service: CounterService = Depends(get_counter_service)
):
    """
    Allow a voter to verify their vote was counted correctly.
    
    The voter provides their N2 fingerprint to check:
    - If their vote was counted
    - What status it has (valid, invalid_signature, invalid_n2)
    - What vote was recorded (if valid)
    """
    try:
        counted_vote = counter_service.verify_vote_by_n2(n2=request.n2)
        
        if not counted_vote:
            return {
                "found": False,
                "message": "No vote found with this N2 fingerprint"
            }
        
        return {
            "found": True,
            "status": counted_vote.status.value,
            "vote": counted_vote.vote if counted_vote.status.value == "valid" else None,
            "message": {
                "valid": "Your vote was counted successfully",
                "invalid_signature": "Your vote was rejected due to invalid signature",
                "invalid_n2": "Your vote was rejected due to invalid N2 fingerprint"
            }.get(counted_vote.status.value, "Unknown status")
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error verifying vote: {str(e)}"
        )