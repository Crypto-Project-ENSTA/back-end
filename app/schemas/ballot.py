from pydantic import BaseModel
from typing import Optional


class Ballot(BaseModel):
   
    vote: str          
    N2: str            
    random_bits: str   

    # --- set during mask_ballot ---
    m: Optional[int] = None        # the ballot converted to a number (needed by unmask)
    k: Optional[int] = None        # the secret blinding factor (NEVER sent anywhere)
    m_prime: Optional[int] = None  # the blinded ballot sent to admin

    # --- set during unmask_signature ---
    admin_signature: Optional[int] = None  # the final valid RSA signature


class MaskedBallot(BaseModel):
    # the ONLY thing sent to the admin — one number, nothing else
    m_prime: int


class MaskedSignature(BaseModel):
    # the ONLY thing the admin sends back — one number, nothing else
    m_pp: int