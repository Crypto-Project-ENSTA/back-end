from dataclasses import dataclass

@dataclass
class VoterBallotDTO:
    vote: str
    n2: str
    random_bits: str

    def __str__(self):
        return f"({self.vote},{self.n2},{self.random_bits})"