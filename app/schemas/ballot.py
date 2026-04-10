from pydantic import BaseModel
from typing import Optional

class Ballot(BaseModel):
    vote: str
    N2: str
    random_bits: str

    masked_ballot: Optional[str] = None
    masked_signature: Optional[str] = None
    admin_signature: Optional[str] = None