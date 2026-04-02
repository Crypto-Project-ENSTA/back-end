import secrets
import hashlib


def generate_nonce(length: int = 32) -> str:
    """
    Generate a secure random string (N1 or N2)
    """
    return secrets.token_hex(length)


def hash_n2(n2: str) -> str:
    """
    Hash N2 using SHA-256
    """
    return hashlib.sha256(n2.encode()).hexdigest()


def hash_n2(n2: str) -> str:
    if not n2:
        raise ValueError("n2 cannot be empty")
    return hashlib.sha256(n2.encode()).hexdigest()