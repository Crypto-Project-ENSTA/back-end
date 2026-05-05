from typing import Optional

from pydantic import BaseModel, Field


class VerifyVoteResponse(BaseModel):
    found: bool = Field(..., description="Whether a vote was found for the given N2 fingerprint")
    status: Optional[str] = Field(None, description="Vote status: `valid`, `invalid_signature`, or `invalid_n2`")
    vote: Optional[str] = Field(None, description="The recorded vote choice — only present when status is `valid`")
    message: str = Field(..., description="Human-readable explanation of the vote status")

    model_config = {
        "json_schema_extra": {
            "examples": {
                "valid_vote": {
                    "summary": "Vote found and valid",
                    "value": {
                        "found": True,
                        "status": "valid",
                        "vote": "A",
                        "message": "Your vote was counted successfully"
                    }
                },
                "invalid_signature": {
                    "summary": "Vote rejected — bad signature",
                    "value": {
                        "found": True,
                        "status": "invalid_signature",
                        "vote": None,
                        "message": "Your vote was rejected due to invalid signature"
                    }
                },
                "not_found": {
                    "summary": "No vote found",
                    "value": {
                        "found": False,
                        "status": None,
                        "vote": None,
                        "message": "No vote found with this N2 fingerprint"
                    }
                }
            }
        }
    }
