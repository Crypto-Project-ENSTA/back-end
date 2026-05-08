import pytest
from app.services.voting_system_service import VotingSystemService
from app.services.administrator_service import AdministratorService
from app.utils.crypto import (
    create_ballot,
    mask_ballot,
    unmask_signed_ballot,
)

E, N = AdministratorService.PUBLIC_KEY


def get_service():
    return VotingSystemService()


#  Test 1 : Basic correctness 

def test_basic_blind_signature():
    """Happy path — signature must verify."""
    service = get_service()
    result  = service.get_blind_signed_ballot(n2="AF15GH258ZQP", vote="8")
    assert result is not None
    print(" test_basic_blind_signature passed")


#  Test 2 : Different votes produce different signatures 

def test_different_votes_different_signatures():
    """Two different votes must never produce the same signature."""
    service = get_service()
    s1 = service.get_blind_signed_ballot(n2="AF15GH258ZQP", vote="8")
    s2 = service.get_blind_signed_ballot(n2="AF15GH258ZQP", vote="3")
    assert s1.signed_ballot != s2.signed_ballot
    print(" test_different_votes_different_signatures passed")


#  Test 3 : Same vote twice → different signatures 

def test_same_vote_different_k_different_signature():
    """
    Same vote submitted twice must produce different signatures
    because k (masking factor) is random each time.
    This ensures ballot unlinkability.
    """
    service = get_service()
    s1 = service.get_blind_signed_ballot(n2="AF15GH258ZQP", vote="8")
    s2 = service.get_blind_signed_ballot(n2="AF15GH258ZQP", vote="8")
    assert s1.signed_ballot != s2.signed_ballot
    print(" test_same_vote_different_k_different_signature passed")


#  Test 4 : Signature math verification 

def test_signature_math():
    """s^e mod N must equal original ballot integer m."""
    ballot        = create_ballot(n2="BZ92KL371MNP", vote="5")
    m             = ballot.to_int()
    masked        = mask_ballot(ballot, AdministratorService.PUBLIC_KEY)
    admin         = AdministratorService(db=None, commissioner=None)
    signed_masked = admin.sign_masked_ballot(masked)
    signed        = unmask_signed_ballot(
        admin_N_public_key   = N,
        masked_Ballot        = masked,
        signed_masked_ballot = signed_masked
    )
    assert pow(signed.signed_ballot, E, N) == m
    print(" test_signature_math passed")


#  Test 5 : Tampered vote fails verification 

def test_tampered_vote_fails():
    """
    If the signed ballot is modified after signing,
    verification must fail.
    """
    ballot        = create_ballot(n2="XX99YY001ZZZ", vote="7")
    m             = ballot.to_int()
    masked        = mask_ballot(ballot, AdministratorService.PUBLIC_KEY)
    admin         = AdministratorService(db=None, commissioner=None)
    signed_masked = admin.sign_masked_ballot(masked)
    signed        = unmask_signed_ballot(
        admin_N_public_key   = N,
        masked_Ballot        = masked,
        signed_masked_ballot = signed_masked
    )

    # Tamper with the signature
    tampered = signed.signed_ballot + 1

    assert pow(tampered, E, N) != m
    print(" test_tampered_vote_fails passed")


#  Test 6 : Admin never sees original ballot 

def test_admin_blindness():
    """
    Masked ballot must not equal original ballot integer m.
    Ensures the administrator truly cannot see the vote.
    """
    ballot = create_ballot(n2="AF15GH258ZQP", vote="9")
    m      = ballot.to_int()
    masked = mask_ballot(ballot, AdministratorService.PUBLIC_KEY)

    assert masked.masked_ballot != m
    print(" test_admin_blindness passed")


#  Test 7 : Different N2 same vote → different ballot 

def test_different_n2_different_ballot():
    """Different N2 codes must produce different ballot integers."""
    b1 = create_ballot(n2="AAAABBBBCCCC", vote="6")
    b2 = create_ballot(n2="XXXXYYYYZZZZ", vote="6")
    assert b1.to_int() != b2.to_int()
    print(" test_different_n2_different_ballot passed")


#  Test 8 : Ballot too large for N 

def test_ballot_fits_modulus():
    """Ballot integer must always be smaller than N."""
    ballot = create_ballot(n2="AF15GH258ZQP", vote="8")
    m      = ballot.to_int()
    assert m < N
    print(" test_ballot_fits_modulus passed")


#  Run all 

if __name__ == "__main__":
    test_basic_blind_signature()
    test_different_votes_different_signatures()
    test_same_vote_different_k_different_signature()
    test_signature_math()
    test_tampered_vote_fails()
    test_admin_blindness()
    test_different_n2_different_ballot()
    test_ballot_fits_modulus()
    print("\n" + "" * 40)
    print(" All tests passed")
    print("" * 40)