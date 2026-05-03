from pydantic import BaseModel, Field


class VoteSubmission(BaseModel):
    n2: str = Field(..., description="Voter's unique nonce (n2)")
    vote: str = Field(..., description="The voter's choice")
    