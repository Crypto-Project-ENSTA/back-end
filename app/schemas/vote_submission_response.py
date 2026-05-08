from pydantic import BaseModel, Field


class SubmitVoteResponse(BaseModel):
    status: str = Field(..., description="`success` when the ballot was accepted")
    message: str = Field(..., description="Human-readable confirmation")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Vote submitted successfully and sent to anonymizer"
            }
        }
    }
