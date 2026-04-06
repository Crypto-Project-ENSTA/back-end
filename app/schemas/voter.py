from pydantic import BaseModel


class Voter(BaseModel):
    email : str 