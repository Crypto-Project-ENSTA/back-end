from fastapi import APIRouter
from app.schemas.voting_system_config_schema import voting_system_config_schema,VotingSystemConfigSchema

"""
Router: Voting System Configuration API

This module defines an endpoint to retrieve the hardcoded voting system configuration.
The configuration includes:
- Number of voters
- Vote theme / ballot question
- Exactly 4 predefined choices

Endpoint:
GET /config/voting-system-config
Returns the configuration as a JSON object using the VotingSystemConfigSchema Pydantic model.
"""
router = APIRouter(prefix ='/config')

@router.get('/voting-system-config',response_model = VotingSystemConfigSchema)
def get_voting_system_config():
    return voting_system_config_schema
