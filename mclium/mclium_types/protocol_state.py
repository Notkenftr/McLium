from enum import Enum

class ProtocolState(Enum):
    HANDSHAKE = 0
    STATUS = 1
    LOGIN = 2
    PLAY = 3
