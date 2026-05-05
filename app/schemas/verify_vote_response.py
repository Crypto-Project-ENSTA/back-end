from typing import Optional

from pydantic import BaseModel, Field


class VerifyVoteResponse(BaseModel):
    found: bool = Field(..., description="Whether a vote was found for the given N2 fingerprint")
    status: Optional[str] = Field(None, description="Vote status: `valid`, `invalid_signature`, or `invalid_n2`")
    vote: Optional[str] = Field(None, description="The recorded vote choice — only present when status is `valid`")
    message: str = Field(..., description="Human-readable explanation of the vote status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "found": True,
                "status": "valid",
                "vote": "A",
                "message": "Your vote was counted successfully"
            }
        }
    }