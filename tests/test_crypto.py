from app.utils.crypto import generate_nonce, hash_n2, create_ballot,mask_ballot,sign_masked_ballot
from app.services.voting_system_service import VotingSystemService
# generate nonce
n2 = generate_nonce()
print("Generated N2:", n2)

# hash it
hashed = hash_n2(n2)
print("Hashed N2:", hashed)

print('start creating')
votingSysService = VotingSystemService()
votingSysService.get_blind_signed_ballot(n2=n2,vote='walid')
print('finishing')
# ballot = create_ballot(n2=n2,vote="walid")
# print('the ballot is :',ballot)
# print('the int ballot is :', ballot.to_int())

# masked_ballot = mask_ballot(voter_ballot=ballot,administrator_pub_key=[12,10**617])# N = 2048 bits
# print('the masked ballot is :',masked_ballot)

# signed_masked_ballot = sign_masked_ballot(masked_ballot=masked_ballot,admin_N_public_key=10**617,admin_private_key=100)
# print('the signed masked ballot is :',signed_masked_ballot)
