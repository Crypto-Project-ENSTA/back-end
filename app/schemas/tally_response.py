from pydantic import BaseModel, Field


class CandidateTally(BaseModel):
    count: int = Field(..., description="Number of valid votes for this candidate")
    percentage: float = Field(..., description="Percentage of total valid votes")

class TallyResponse(BaseModel):
    total_votes: int = Field(..., description="Total number of valid votes counted")
    tally: dict[str, CandidateTally] = Field(..., description="Vote count and percentage per candidate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_votes": 5,
                "tally": {
                    "A": {"count": 3, "percentage": 60.0},
                    "B": {"count": 2, "percentage": 40.0}
                }
            }
        }
    }


class EmptyTallyResponse(BaseModel):
    message: str = Field(..., description="Informational message when no votes exist")
    tally: dict = Field(default={}, description="Empty tally")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "No valid votes counted yet",
                "tally": {}
            }
        }
    }