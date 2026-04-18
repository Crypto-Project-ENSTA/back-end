from dataclasses import dataclass

@dataclass
class VoterBallotDTO:
    vote: str
    n2: str
    random_bits: str

    def __str__(self):
        return f"({self.vote},{self.n2},{self.random_bits})"
    
    def to_int(self) -> int:
        """Convert ballot to integer for RSA operations"""
        # Example: converting "Hi" to an integer

        # Step 1: string to bytes
        # "Hi" → b'Hi'
        # ASCII values:
        # 'H' = 72, 'i' = 105
        # so bytes = [72, 105]

        # Step 2: interpret bytes as a base-256 number (big-endian)
        # value = 72 * 256^1 + 105 * 256^0

        # Step 3: compute
        # 72 * 256 = 18432
        # 105 * 1   = 105
        # total = 18432 + 105 = 18537

        # Final result:
        # "Hi" → 18537
        message = str(self)
        return int.from_bytes(message.encode(), byteorder='big')# 'big' means big-indian
    


@dataclass
class MaskedBallotDTO:
    masked_message: int
    k: int
    
    def __str__(self):
        return f'{self.masked_message},{self.k}'