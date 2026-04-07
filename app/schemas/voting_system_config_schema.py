from pydantic import BaseModel
# from app.backend_config.voting_system_config import VotingSystemConfig


class VotingSystemConfigSchema(BaseModel):
    
    emails_sent: bool
    num_voters : int
    vote_theme : str
    choices : list[str]
    
# # create instance directly from hardcoded class
# voting_system_config_schema = VotingSystemConfigSchema(
#     num_voters=VotingSystemConfig.num_voters,
#     vote_theme=VotingSystemConfig.vote_theme,
#     choices=list(VotingSystemConfig.choices)
# )