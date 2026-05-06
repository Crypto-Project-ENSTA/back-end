from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.voting_system_config_repo import get_voting_config, update_voting_config
from app.schemas.update_voting_config import UpdateVotingConfigSchema
from app.schemas.voting_system_config_schema import VotingSystemConfigSchema

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

@router.get('/voting-system-config', response_model=VotingSystemConfigSchema)
def get_voting_system_config(db: Session = Depends(get_db)):
    config = get_voting_config(db)

    return VotingSystemConfigSchema(
        num_voters=config.num_voters,
        vote_theme=config.vote_theme,
        choices=config.choices or []
    )
    
@router.patch(
    "/voting-system-config",
    response_model=VotingSystemConfigSchema,
    summary="Update voting system config",
    description="Update one or more voting config fields. Only provided fields will be modified.",
    responses={
        200: {"description": "Config updated successfully"},
    },
)
def patch_voting_system_config(
    updates: UpdateVotingConfigSchema,
    db: Session = Depends(get_db)
):
    config = update_voting_config(db=db, updates=updates)

    return VotingSystemConfigSchema(
        num_voters=config.num_voters,
        vote_theme=config.vote_theme,
        choices=config.choices or []
    )