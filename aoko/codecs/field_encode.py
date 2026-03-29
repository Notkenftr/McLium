from aoko.codecs.encode import Encode
from aoko.enums.packet import AokoPacketFieldType

def _encode_field(field,debug=False):
    prefix = b""

    ft = field.field_type
    value = field.value

    if debug:
        print(f"[Field] Type={ft} Value={value}")

    if ft == AokoPacketFieldType.VARINT:
        data = Encode.EncodeVarInt(value)
    elif ft == AokoPacketFieldType.UNSIGNED_BYTE:
        data = Encode.EncodeUnsignedByte(value)
    elif ft == AokoPacketFieldType.BYTE:
        data = Encode.EncodeByte(value)
    elif ft == AokoPacketFieldType.STRING:
        data = Encode.EncodeString(value)
    elif ft == AokoPacketFieldType.BOOL:
        data = Encode.EncodeBool(value)
    elif ft == AokoPacketFieldType.INT:
        data = Encode.EncodeInt(value)
    elif ft == AokoPacketFieldType.UNSIGNED_SHORT:
        data = Encode.EncodeUnsignedShort(value)
    elif ft == AokoPacketFieldType.LONG:
        data = Encode.EncodeLong(value)
    elif ft == AokoPacketFieldType.UUID:
        data = Encode.EncodeUUID(value)
    elif ft == AokoPacketFieldType.FLOAT:
        data = Encode.EncodeFloat(value)
    elif ft == AokoPacketFieldType.DOUBLE:
        data = Encode.EncodeDouble(value)
    elif ft == AokoPacketFieldType.POSITION:
        data = Encode.EncodePosition(*value)
    elif ft == AokoPacketFieldType.VARLONG:
        data = Encode.EncodeVarLong(value)
    else:
        raise ValueError(f"Unsupported field type: {ft}")

    return prefix + data
