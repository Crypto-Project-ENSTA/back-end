from app.utils.crypto import generate_nonce, hash_n2

# generate nonce
n2 = generate_nonce()
print("Generated N2:", n2)

# hash it
hashed = hash_n2(n2)
print("Hashed N2:", hashed)