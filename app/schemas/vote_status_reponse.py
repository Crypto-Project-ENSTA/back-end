from pydantic import BaseModel

from app.models.voting_system_config_model import VotingStatus


class VoteStatusResponse(BaseModel):
    voting_status: VotingStatus
