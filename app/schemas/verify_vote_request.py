from pydantic import BaseModel


class VerifyVoteRequest(BaseModel):
    n2: str