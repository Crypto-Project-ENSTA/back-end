from pydantic import BaseModel, Field


class TallyResponse(BaseModel):
    total_votes: int = Field(..., description="Total number of valid votes counted")
    tally: dict[str, int] = Field(..., description="Vote count per candidate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_votes": 5,
                "tally": {"A": 3, "B": 2}
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