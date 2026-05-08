from pydantic import BaseModel, Field


class CandidateTally(BaseModel):
    candidate: str
    count: int
    percentage: float

class TallyResponse(BaseModel):
    total_votes: int
    tally: list[CandidateTally]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_votes": 5,
                "tally": [
                    {"candidate": "A", "count": 3, "percentage": 60.0},
                    {"candidate": "B", "count": 2, "percentage": 40.0},
                ]
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