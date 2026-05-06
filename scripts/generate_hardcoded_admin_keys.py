# ============================================================
# This script was used to manually generate RSA key pairs (E, N, D) and hardcode them
# directly into the service classes. It has been replaced by OpenSSL-generated .pem files
# stored in the keys/ directory and loaded via app/key_loader.py.
# Keeping this file for reference only — do not use in production.
#
# To regenerate keys, run:
#   mkdir keys
#   openssl genrsa -out keys/counter_private.pem 2048
#   openssl rsa -in keys/counter_private.pem -pubout -out keys/counter_public.pem
#   openssl genrsa -out keys/admin_private.pem 2048
#   openssl rsa -in keys/admin_private.pem -pubout -out keys/admin_public.pem
# ============================================================


# import random

# def generate_prime(bits=1024):
#     while True:
#         n = random.getrandbits(bits) | (1 << bits - 1) | 1
#         if is_prime(n):
#             return n

# def is_prime(n, rounds=20):
#     if n < 2: return False
#     if n == 2: return True
#     if n % 2 == 0: return False
#     r, d = 0, n - 1
#     while d % 2 == 0:
#         r += 1; d //= 2
#     for _ in range(rounds):
#         a = random.randrange(2, n - 1)
#         x = pow(a, d, n)
#         if x in (1, n - 1): continue
#         for _ in range(r - 1):
#             x = pow(x, 2, n)
#             if x == n - 1: break
#         else: return False
#     return True

# def mod_inverse(a, m):
#     def ext_gcd(a, b):
#         if a == 0: return b, 0, 1
#         g, x, y = ext_gcd(b % a, a)
#         return g, y - (b // a) * x, x
#     _, x, _ = ext_gcd(a % m, m)
#     return (x % m + m) % m

# print(" Generating 1024-bit primes (N will be 2048 bits)...")

# p   = generate_prime(1024)
# q   = generate_prime(1024)
# N   = p * q
# phi = (p - 1) * (q - 1)
# e   = 65537 # industry standard
# d   = mod_inverse(e, phi)

# print(f"\n# Copy these into AdministratorService:")
# print(f"E = {e}")
# print(f"N = {N}")
# print(f"D = {d}")