from enum import Enum

class AokoPacketFieldType(Enum):
    VARINT = "varint"
    STRING = "string"
    INT = "int"
    BOOL = "bool"
    UUID = "uuid"
    UNSIGNED_SHORT = "unsigned_short"
    UNSIGNED_BYTE = "unsigned_byte"
    LONG = "long"
    BYTE = "byte"
    FLOAT = "float"
    DOUBLE = "double"

    AokoRAWBYTE = 'aokorawbyte'

class AokoPacketBuildMode(Enum):
    BYTEARRAY = "bytearray"
    BYTEPLUS = "byteplus"

class AokoPacketHooker(Enum):
    HEAD = "head"
    AFTER_ENCODE_FIELD = "after_encode_field"
    TAIL = "tail"

class AokoPacketRegister(Enum):
    HOOKER = "hooker"

