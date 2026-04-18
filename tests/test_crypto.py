from app.utils.crypto import generate_nonce, hash_n2, create_ballot,mask_ballot
# generate nonce
n2 = generate_nonce()
print("Generated N2:", n2)

# hash it
hashed = hash_n2(n2)
print("Hashed N2:", hashed)

ballot = create_ballot(n2=n2,vote="walid")
print('the ballot is :',ballot)
print('the int ballot is :', ballot.to_int())

masked_ballot = mask_ballot(voter_ballot=ballot,administrator_pub_key=[12,10**617])# N = 2048 bits
print('the masked ballot is :',masked_ballot)