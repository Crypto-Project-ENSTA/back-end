from pydantic import BaseModel, Field


class RegisterResponse(BaseModel):
    status: str = Field(..., description="`success` or `error`")
    message: str = Field(..., description="Human-readable result of the registration attempt")
    voter: str = Field(..., description="Email address of the voter concerned")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Voter registered successfully",
                "voter": "alice@example.com"
            }
        }
    }