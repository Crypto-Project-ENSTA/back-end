from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.tally_response import TallyResponse
from app.schemas.verify_vote_request import VerifyVoteRequest
from app.schemas.verify_vote_response import VerifyVoteResponse
from app.services.counter_service import CounterService
from app.dependencies import get_counter_service

router = APIRouter(prefix="/results")



@router.get("/tally",response_model=TallyResponse,
    summary="Get election results tally",
    description="""
Returns the current vote counts for all candidates, along with the total
number of valid votes processed so far.

Only **valid** votes are included in the tally — rejected votes
(`invalid_signature`, `invalid_n2`) are excluded from all counts.
""",
    responses={
        200: {
            "description": "Tally returned successfully (may be empty if no votes yet)",
            "content": {
                "application/json": {
                    "examples": {
                        "with_votes": {
                            "summary": "Election in progress",
                            "value": {"total_votes": 5, "tally": {"A": 3, "B": 2}}
                        },
                        "no_votes": {
                            "summary": "No votes counted yet",
                            "value": {"message": "No valid votes counted yet", "tally": {}}
                        }
                    }
                }
            }
        },
        500: {"description": "Internal server error while retrieving results"}
    }
)
def get_election_results(
    counter_service: CounterService = Depends(get_counter_service)
):

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
        raise HTTPException(status_code=500, detail=f"Error retrieving results: {str(e)}")

@router.post("/verify-vote",
    response_model=VerifyVoteResponse,
    summary="Verify a vote by N2 fingerprint",
    description="""
Allows a voter to confirm whether their vote was received and counted correctly.

The voter submits their **N2 fingerprint** and receives back:
- Whether a matching vote was found in the system
- The vote's current status (`valid`, `invalid_signature`, `invalid_n2`)
- The recorded vote choice (only disclosed when the vote is `valid`)

This endpoint does **not** mutate any state — it is read-only.
""",
    responses={
        200: {"description": "Lookup completed — check `found` and `status` fields in the response"},
        500: {"description": "Internal server error while verifying the vote"}
    }
)
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
                "status": None,
                "vote": None,
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