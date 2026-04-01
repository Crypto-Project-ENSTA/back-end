from fastapi import APIRouter
from app.schemas.voting_system_config_schema import voting_system_config_schema
router = APIRouter(prefix ='/config')


@router.get('/voting-system-config')
def get_voting_system_config():
    return voting_system_config_schema
