from pydantic import BaseModel, Field


class N1CheckResponse(BaseModel):
    is_N1_exist: bool = Field(
        ...,
        description=(
            "`true` if the N1 code was recognised by the commissioner and has been "
            "stored in the session for the upcoming vote submission. "
            "`false` if the code is unknown."
        )
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "is_N1_exist": True
            }
        }
    }