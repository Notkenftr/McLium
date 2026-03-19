from mclium.mclium_types import PacketFieldType
from mclium.api.network.mc_protocol import Encode

def _EncodeField(field, debug=False) -> bytes:
    if field.optional:
        if field.value is None:
            if debug:
                print("[Field] Optional = False")
            return Encode.EncodeBool(False)
        prefix = Encode.EncodeBool(True)
    else:
        prefix = b""

    ft = field.field_type
    value = field.value

    if debug:
        print(f"[Field] Type={ft} Value={value}")

    if ft == PacketFieldType.VARINT:
        return prefix + Encode.EncodeVarInt(value)

    elif ft == PacketFieldType.STRING:
        return prefix + Encode.EncodeString(value)

    elif ft == PacketFieldType.BOOL:
        return prefix + Encode.EncodeBool(value)

    elif ft == PacketFieldType.INT:
        return prefix + Encode.EncodeInt(value)

    elif ft == PacketFieldType.UNSIGNED_SHORT:
        return prefix + Encode.EncodeUnsignedShort(value)

    elif ft == PacketFieldType.LONG:
        return prefix + Encode.EncodeLong(value)

    elif ft == PacketFieldType.UUID:
        return prefix + Encode.EncodeUUID(value)

    elif ft == PacketFieldType.FLOAT:
        return prefix + Encode.EncodeFloat(value)

    elif ft == PacketFieldType.DOUBLE:
        return prefix + Encode.EncodeDouble(value)

    elif ft == PacketFieldType.BYTE:
        return prefix + Encode.EncodeByte(value)

    elif ft == PacketFieldType.POSITION:
        return prefix + Encode.EncodePosition(*value)

    elif ft == PacketFieldType.VARLONG:
        return prefix + Encode.EncodeVarLong(value)

    raise ValueError(f"Unsupported field type: {ft}")
