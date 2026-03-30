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

    _AOKORAWBYTE = "aokorawbyte"

class AokoPacketBuildMode(Enum):
    BYTEARRAY = "bytearray"
    BYTEPLUS = "byteplus"

class AokoPacketHooker(Enum):
    BEFORE_BUILD = "before_build"
    BEFORE_PACKET_ID_ENCODE = "before_packet_id_encode"
    AFTER_PACKET_ID_ENCODE = "after_packet_id_encode"
    BEFORE_ENCODE_FIELD = "on_encode_field"
    AFTER_ENCODE_FIELD = "after_encode_field"
    BEFORE_PACKET_LENGTH_ENCODE = "before_packet_length_encode"
    AFTER_PACKET_LENGTH_ENCODE = "after_packet_length_encode"
    AFTER_BUILD = "after_build"

class AokoPacketRegister(Enum):
    HOOKER = "hooker"

