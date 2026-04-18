from app.utils.crypto import generate_nonce, hash_n2, create_ballot
# generate nonce
n2 = generate_nonce()
print("Generated N2:", n2)

# hash it
hashed = hash_n2(n2)
print("Hashed N2:", hashed)

ballot = create_ballot(n2=n2,vote="walid")
print('the ballot is :',ballot)