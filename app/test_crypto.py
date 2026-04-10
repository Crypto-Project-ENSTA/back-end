from app.utils.crypto import create_ballot, mask_ballot, request_signature, unmask_signature

# Step 1: create ballot
ballot = create_ballot("YES", "123", "abc")

# Step 2: mask it
ballot = mask_ballot(ballot)

# Step 3: simulate admin signing
ballot.masked_signature = request_signature(ballot.masked_ballot)

# Step 4: unmask
ballot = unmask_signature(ballot)

# print result
print(ballot)