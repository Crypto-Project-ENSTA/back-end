from pydantic import BaseModel


class VoteStatusResponse(BaseModel):
    voting_status: str

