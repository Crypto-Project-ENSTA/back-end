import secrets
import hashlib
import secrets
import string


"""
Generate a cryptographically secure random alphanumeric code (nonce).

This function creates a random string of a specified length using
uppercase English letters (A–Z) and digits (0–9). It relies on the
`secrets` module to ensure strong randomness suitable for security-
sensitive contexts such as authentication tokens, session identifiers,
or one-time codes.

The total number of possible combinations is 36^length, providing
a very large search space which offers(10 + 26)^12 ≈ 10^18

Example:
    >>> generate_nonce(12)
    'AF15GH258ZQP'
"""

def generate_nonce(length: int = 12) -> str:
    alphabet = string.ascii_uppercase + string.digits  # A-Z + 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))

"""
Hash a nonce (N2) using SHA-256.

    Process explanation:
    1. The nonce `n2` is initially a string, e.g., "AF15GH258ZQP".
    2. `n2.encode()` converts the string into bytes because the SHA-256
       hashing function works on bytes, not on regular strings.
       Example: "AF15GH258ZQP" -> b'AF15GH258ZQP'
    3. `hashlib.sha256(...)` computes the SHA-256 hash of the byte sequence.
       - SHA-256 is a cryptographic hash function that is:
         - One-way: the original string cannot be recovered from the hash.
         - Fixed-length: always produces 256-bit (64 hex character) output.
         - Deterministic: the same input always produces the same output.
    4. `.hexdigest()` converts the raw binary hash into a readable
       hexadecimal string, suitable for storing or sending over a network.
       Example: b'\x3a\x7d\x8e...' -> '3a7d8e3f1c2b4f6a...'
    5. The resulting string is returned as the hashed representation of the nonce.

"""
def hash_n2(n2: str) -> str:
    if not n2:
        raise ValueError("n2 cannot be empty")
    return hashlib.sha256(n2.encode()).hexdigest()
from app.schemas.ballot import Ballot


def create_ballot(vote: str, N2: str, random_bits: str) -> Ballot:
    return Ballot(
        vote=vote,
        N2=N2,
        random_bits=random_bits
    )


def mask_ballot(ballot: Ballot) -> Ballot:
    masked_value = f"masked({ballot.vote}-{ballot.N2}-{ballot.random_bits})"
    ballot.masked_ballot = masked_value
    return ballot


def request_signature(masked_ballot: str) -> str:
    return f"signed({masked_ballot})"


def unmask_signature(ballot: Ballot) -> Ballot:
    if not ballot.masked_signature:
        raise ValueError("Masked signature is missing")

    admin_signature = ballot.masked_signature.replace("signed(masked(", "").replace("))", ")")
    ballot.admin_signature = admin_signature
    return ballot