# schemas
from typing import Optional
from pydantic import BaseModel


class UpdateVotingConfigSchema(BaseModel):
    num_voters: Optional[int] = None
    vote_theme: Optional[str] = None
    choices: Optional[list[str]] = None
