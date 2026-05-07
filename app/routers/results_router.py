from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.counted_votes_repository import get_tally
from app.schemas.tally_response import TallyResponse
from app.schemas.verify_vote_request import VerifyVoteRequest
from app.schemas.verify_vote_response import VerifyVoteResponse
from app.services.counter_service import CounterService
from app.dependencies import get_counter_service

router = APIRouter(prefix="/results")



@router.get(
    "/tally",
    response_model=TallyResponse,
    summary="Get election results tally",
    description="""
Returns the current vote counts and percentages for all candidates, along with the total
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
                            "value": {
                                "total_votes": 5,
                                "tally": [
                                    {"candidate": "A", "count": 3, "percentage": 60.0},
                                    {"candidate": "B", "count": 2, "percentage": 40.0},
                                ],
                            },
                        },
                        "no_votes": {
                            "summary": "No votes counted yet",
                            "value": {"total_votes": 0, "tally": []},
                        },
                    }
                }
            },
        },
        500: {"description": "Internal server error while retrieving results"},
    },
)
def get_election_results(db: Session = Depends(get_db),counter : CounterService =Depends(get_counter_service)):
    try:
        tally = counter.get_results()
        return TallyResponse(
            total_votes=sum(c["count"] for c in tally),
            tally=tally
        )
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

## Possible Outcomes

### 1. Vote Not Found
**Condition:** No vote exists in the system with the provided N2 fingerprint.

**Response:**
```json
{
    "found": false,
    "status": null,
    "vote": null,
    "message": "No vote found with this N2 fingerprint"
}
```

**Possible Reasons:**
- The voter hasn't submitted a vote yet
- Incorrect N2 fingerprint was provided
- Vote was never received by the system

---

### 2. Vote Found - Valid
**Condition:** Vote was received, validated successfully, and counted.

**Response:**
```json
{
    "found": true,
    "status": "valid",
    "vote": "<voter's choice>",
    "message": "Your vote was counted successfully"
}
```

**Details:**
- Both the digital signature and N2 fingerprint passed validation
- The vote is included in the final tally
- The actual vote choice is disclosed to the voter

---

### 3. Vote Found - Invalid Signature
**Condition:** Vote was received but failed digital signature verification.

**Response:**
```json
{
    "found": true,
    "status": "invalid_signature",
    "vote": null,
    "message": "Your vote was rejected due to invalid signature"
}
```

**Details:**
- The digital signature could not be verified against the registered public key
- The vote was **not** counted in the final tally
- Vote choice is **not** disclosed (potential tampering detected)

**Possible Reasons:**
- Vote data was tampered with after signing
- Wrong private key was used to sign the vote
- Signature corruption during transmission

---

### 4. Vote Found - Invalid N2
**Condition:** Vote was received but failed N2 fingerprint validation.

**Response:**
```json
{
    "found": true,
    "status": "invalid_n2",
    "vote": null,
    "message": "Your vote was rejected due to invalid N2 fingerprint"
}
```

**Details:**
- The N2 fingerprint validation failed
- The vote was **not** counted in the final tally
- Vote choice is **not** disclosed (potential eligibility issue)

**Possible Reasons:**
- N2 fingerprint doesn't match the voter's registered credentials
- Voter registration was not properly completed
- N2 fingerprint was computed incorrectly during vote submission

""",
    responses={
        200: {
            "description": "Lookup completed — check `found` and `status` fields in the response",
            "content": {
                "application/json": {
                    "examples": {
                        "vote_not_found": {
                            "summary": "No vote found",
                            "value": {
                                "found": False,
                                "status": None,
                                "vote": None,
                                "message": "No vote found with this N2 fingerprint"
                            }
                        },
                        "vote_valid": {
                            "summary": "Valid vote (counted)",
                            "value": {
                                "found": True,
                                "status": "valid",
                                "vote": "Candidate A",
                                "message": "Your vote was counted successfully"
                            }
                        },
                        "vote_invalid_signature": {
                            "summary": "Invalid signature (not counted)",
                            "value": {
                                "found": True,
                                "status": "invalid_signature",
                                "vote": None,
                                "message": "Your vote was rejected due to invalid signature"
                            }
                        },
                        "vote_invalid_n2": {
                            "summary": "Invalid N2 fingerprint (not counted)",
                            "value": {
                                "found": True,
                                "status": "invalid_n2",
                                "vote": None,
                                "message": "Your vote was rejected due to invalid N2 fingerprint"
                            }
                        }
                    }
                }
            }
        },
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