from pathlib import Path
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
KEYS_DIR = Path("keys")

counter_private_key = load_pem_private_key(
    (KEYS_DIR / "counter_private.pem").read_bytes(), password=None
)
counter_public_key = load_pem_public_key(
    (KEYS_DIR / "counter_public.pem").read_bytes()
)
admin_private_key = load_pem_private_key(
    (KEYS_DIR / "admin_private.pem").read_bytes(), password=None
)
admin_public_key = load_pem_public_key(
    (KEYS_DIR / "admin_public.pem").read_bytes()
)