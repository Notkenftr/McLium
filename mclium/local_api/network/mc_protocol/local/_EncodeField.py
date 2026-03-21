from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Encode

def _EncodeField(field, debug=False) -> bytes:
    prefix = b""  # ignore optional prefix for most serverbound packets

    ft = field.field_type
    value = field.value

    if debug:
        print(f"[Field] Type={ft} Value={value}")

    if ft == PacketFieldType.VARINT:
        data = Encode.EncodeVarInt(value)
    elif ft == PacketFieldType.UNSIGNED_BYTE:
        data = Encode.EncodeUnsignedByte(value)
    elif ft == PacketFieldType.BYTE:
        data = Encode.EncodeByte(value)
    elif ft == PacketFieldType.STRING:
        data = Encode.EncodeString(value)
    elif ft == PacketFieldType.BOOL:
        data = Encode.EncodeBool(value)
    elif ft == PacketFieldType.INT:
        data = Encode.EncodeInt(value)
    elif ft == PacketFieldType.UNSIGNED_SHORT:
        data = Encode.EncodeUnsignedShort(value)
    elif ft == PacketFieldType.LONG:
        data = Encode.EncodeLong(value)
    elif ft == PacketFieldType.UUID:
        data = Encode.EncodeUUID(value)
    elif ft == PacketFieldType.FLOAT:
        data = Encode.EncodeFloat(value)
    elif ft == PacketFieldType.DOUBLE:
        data = Encode.EncodeDouble(value)
    elif ft == PacketFieldType.POSITION:
        data = Encode.EncodePosition(*value)
    elif ft == PacketFieldType.VARLONG:
        data = Encode.EncodeVarLong(value)
    else:
        raise ValueError(f"Unsupported field type: {ft}")

    return prefix + data
