import os
from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

KEYS_DIR = Path("keys")

def _load_key(env_var: str, pem_file: str) -> bytes:
    # Production: load from environment variable
    value = os.getenv(env_var)
    if value:
        return value.replace("\\n", "\n").encode()
    
    # Local: load from .pem file
    pem_path = KEYS_DIR / pem_file
    if pem_path.exists():
        return pem_path.read_bytes()
    
    raise RuntimeError(f"No key found: set {env_var} or provide keys/{pem_file}")

counter_private_key = load_pem_private_key(_load_key("COUNTER_PRIVATE_KEY", "counter_private.pem"), password=None)
counter_public_key  = load_pem_public_key(_load_key("COUNTER_PUBLIC_KEY",  "counter_public.pem"))
admin_private_key   = load_pem_private_key(_load_key("ADMIN_PRIVATE_KEY",  "admin_private.pem"), password=None)
admin_public_key    = load_pem_public_key(_load_key("ADMIN_PUBLIC_KEY",    "admin_public.pem"))