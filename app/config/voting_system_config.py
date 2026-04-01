from typing import Final

class VotingSystemConfig:
    # here all values needs to be harcoded .
    # we use final so we can't change the values (read-only)
    num_voters: Final[int] = 5
    vote_theme: Final[str] = 'Favorite Programming Language'
    choices: Final[tuple[str, ...]] = ("Python", "JavaScript", "C++", "Java")
    # ... : accepts any number of strings, not a fixed length
