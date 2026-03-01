from enum import Enum


class PacketFieldType(Enum):
    VARINT = "varint"
    STRING = "string"
    INT = "int"
    BOOL = "bool"
    UUID = "uuid"