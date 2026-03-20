from enum import Enum


class PacketFieldType(Enum):
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
