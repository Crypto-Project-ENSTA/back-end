from pydantic import BaseModel

class VotingSystemConfigSchema(BaseModel):
    num_voters : int
    vote_theme : str
    choices : list[str]