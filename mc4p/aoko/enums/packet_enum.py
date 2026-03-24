from enum import Enum

class AokoPacketExtendMode(Enum):
    """
    BYTEARRAY:
        Use when building packets incrementally with frequent mutations.
        Best for small packets or dynamic construction.

    PLUS:
        Use when all fields are known beforehand.
        Fastest method (uses b''.join) with minimal memory allocation.
    """
    BYTEARRAY = 1
    PLUS = 2
