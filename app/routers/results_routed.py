from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
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

