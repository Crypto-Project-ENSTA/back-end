import secrets
import hashlib
import string
import random
import math

from app.schemas.ballot import Ballot, MaskedBallot, MaskedSignature
from app.crypto.key_manager import load_public_key, load_private_key


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



def _ballot_to_int(ballot: Ballot) -> int:
    pub = load_public_key("admin")
    n = pub.public_numbers().n
    content = f"{ballot.vote}|{ballot.N2}|{ballot.random_bits}"
    m = int.from_bytes(content.encode("utf-8"), "big")
    return m % n  # m must be < n for RSA math to hold


def _generate_blinding_factor(n: int) -> int:
    while True:
        k = random.randint(2, n - 1)
        if math.gcd(k, n) == 1:  # k must be coprime with n
            return k



def create_ballot(vote: str, N2: str, random_bits: str) -> Ballot:
    return Ballot(vote=vote, N2=N2, random_bits=random_bits)




def mask_ballot(ballot: Ballot) -> MaskedBallot:
    pub = load_public_key("admin")
    pub_numbers = pub.public_numbers()
    e = pub_numbers.e
    n = pub_numbers.n

    m = _ballot_to_int(ballot)
    k = _generate_blinding_factor(n)

    # real RSA blinding: m' = m * k^e mod n
    m_prime = (m * pow(k, e, n)) % n

    # store intermediate values back into ballot for unmask step later
    ballot.m = m
    ballot.k = k
    ballot.m_prime = m_prime

    return MaskedBallot(m_prime=m_prime)



def request_signature(masked_ballot: MaskedBallot) -> MaskedSignature:
    priv = load_private_key("admin")
    priv_numbers = priv.private_numbers()
    d = priv_numbers.d
    n = priv_numbers.public_numbers.n

    # real RSA blind signing: m'' = m'^d mod n
    m_pp = pow(masked_ballot.m_prime, d, n)

    return MaskedSignature(m_pp=m_pp)



def unmask_signature(ballot: Ballot, masked_signature: MaskedSignature) -> Ballot:
    if ballot.k is None:
        raise ValueError("Blinding factor k is missing — was mask_ballot called?")
    if ballot.m is None:
        raise ValueError("Encoded ballot integer m is missing — was mask_ballot called?")

    pub = load_public_key("admin")
    n = pub.public_numbers().n

    # real RSA unblinding: s = m'' * k^-1 mod n
    k_inv = pow(ballot.k, -1, n)
    s = (masked_signature.m_pp * k_inv) % n

    ballot.admin_signature = s
    return ballot